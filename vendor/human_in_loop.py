import os
import json
import logging
import datetime
import traceback
from typing import Optional, Dict, Any

# Import necessary components from campaign_agent
from campaign_agent import CampaignGenerationAgent, CampaignFormat, CampaignFormatBase, logger
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.pydantic_v1 import Field as V1Field # Ensure V1Field is available if needed for revision schema
from pydantic import BaseModel, Field, ValidationError

# --- Configuration ---
MAX_REVISIONS = 5 # Limit the number of revision attempts

# --- Pydantic Model for Revision Request (Optional but good practice) ---
# This helps structure the revision request if needed, though we might just use text feedback
class RevisionRequest(BaseModel):
    """Model for structuring revision feedback."""
    feedback: str = Field(..., description="Specific feedback from the user on what to change.")
    previous_campaign: Dict[str, Any] = Field(..., description="The JSON representation of the campaign to be revised.")

# --- Human-in-the-Loop Manager ---
class HumanInLoopManager:
    """
    Manages the human-in-the-loop process for refining generated campaigns,
    where the vendor name is extracted by the agent.
    """
    def __init__(self, agent: CampaignGenerationAgent):
        self.agent = agent
        logger.info("HumanInLoopManager initialized.")

    def _get_user_feedback(self, current_campaign: CampaignFormat) -> Optional[str]:
        # No changes needed - reads vendor_name from current_campaign
        print("\n--- Current Campaign Draft ---")
        print(f"Campaign ID: {current_campaign.campaign_id}")
        print(f"Timestamp: {current_campaign.timestamp}")
        print(f"Vendor: {current_campaign.vendor_name}") # Reads from object
        print(f"Category: {current_campaign.category}")
        print("Promotions:")
        for promo in current_campaign.promotions:
            print(f"  - {promo}")
        print(f"Notification: {current_campaign.notification}")
        print(f"Slogan: {current_campaign.campaign_slogan}")
        print(f"Message: {current_campaign.campaign_message}")
        print("------------------------------")

        while True:
            feedback = input("Type 'ok' if you approve this campaign, or provide specific feedback (e.g., 'change vendor name to X', 'make slogan funnier'): \n> ") # Added hint about vendor name change
            if feedback.strip().lower() == 'ok':
                logger.info("User approved the campaign.")
                return None
            elif feedback.strip():
                logger.info(f"User provided feedback: {feedback}")
                return feedback.strip()
            else:
                print("Please provide feedback or type 'ok'.")

    def _revise_campaign_prompt(self, previous_campaign: CampaignFormat, feedback: str) -> list:
        # No changes needed - reads vendor_name from previous_campaign
        # Prompt already includes vendor name in context and asks for JSON output including vendor_name
        system_prompt = f"""
        You are a helpful assistant revising a marketing campaign based on user feedback.
        Your goal is to modify the *previous campaign draft* according to the user's instructions while maintaining the core requirements and JSON output format.

        PREVIOUS CAMPAIGN DRAFT (Vendor: '{previous_campaign.vendor_name}'):
        ```json
        {previous_campaign.model_dump_json(indent=4)}
        ```

        USER FEEDBACK FOR REVISION:
        "{feedback}"

        Instructions:
        1. Carefully analyze the user's feedback.
        2. Modify the previous campaign draft ONLY as requested by the feedback. Pay attention if the feedback asks to correct the `vendor_name`.
        3. Ensure all fields (vendor_name, category, promotions, notification, campaign_message, campaign_slogan) are still present and valid according to the original rules.
        4. Output ONLY the revised campaign details in the required JSON format using the provided function call schema. Do not add introductory text.
        """
        human_message_content = [
            {"type": "text", "text": f"Please revise the campaign for vendor '{previous_campaign.vendor_name}' based on the provided feedback."}
        ]
        messages = [ SystemMessage(content=system_prompt), HumanMessage(content=human_message_content) ]
        logger.debug(f"Generated revision prompt messages for vendor: {previous_campaign.vendor_name}")
        return messages

    def revise_campaign(self, previous_campaign: CampaignFormat, feedback: str) -> Optional[CampaignFormat]:
        # No changes needed - vendor_name is handled via CampaignFormatBase validation
        logger.info(f"Revising campaign {previous_campaign.campaign_id} for vendor '{previous_campaign.vendor_name}' based on feedback.")
        prompt_messages = self._revise_campaign_prompt(previous_campaign, feedback)

        try:
            logger.info("Invoking Gemini LLM for revision...")
            chain = self.agent.llm_with_tools | self.agent.output_parser
            response = chain.invoke(prompt_messages)
            logger.debug(f"Raw LLM revision response (parsed function arguments): {response}")

            if not isinstance(response, dict):
                 logger.error(f"LLM revision response is not a dictionary: {type(response)} - {response}")
                 return None
            else:
                response_data = response

            # Validate the revised data using the base model (which includes vendor_name)
            revised_data = CampaignFormatBase(**response_data)

            # Create the final CampaignFormat object
            final_campaign = CampaignFormat(
                **revised_data.dict(), # Includes revised vendor_name if changed by LLM
                campaign_id=previous_campaign.campaign_id,
                timestamp=datetime.datetime.now() # Update timestamp for revision
            )

            logger.info(f"Successfully revised campaign: {final_campaign.campaign_id} (Vendor: {final_campaign.vendor_name})")
            logger.debug(f"Revised campaign details: {final_campaign.model_dump_json(indent=2)}")
            return final_campaign
        
        except ValidationError as e:
            logger.error(f"Pydantic validation error during revision for vendor '{previous_campaign.vendor_name}': {e}", exc_info=True)
            logger.error(f"LLM Revision Response that failed validation: {response}")
            return None
        
        except Exception as e:
            logger.error(f"An error occurred during campaign revision for vendor '{previous_campaign.vendor_name}': {e}", exc_info=True)
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None
        
    def run_interaction(self, catalog_file_path: str) -> Optional[CampaignFormat]: # Removed vendor_name parameter
        """
        Runs the full generate -> review -> revise loop, extracting vendor name initially.

        Args:
            catalog_file_path: Path to the catalog file.

        Returns:
            The final, user-approved CampaignFormat object, or None if aborted/failed.
        """
        logger.info(f"--- Starting HITL process for catalog: {catalog_file_path} ---")

        # 1. Initial Generation (call without vendor_name)
        current_campaign = self.agent.generate_campaign(catalog_file_path)
        if not current_campaign:
            logger.error("Initial campaign generation failed (vendor name extraction might have failed). Aborting HITL process.")
            return None

        # Vendor name is now available from the generated object
        logger.info(f"Initial campaign generated for extracted vendor: '{current_campaign.vendor_name}'")

        # 2. Revision Loop (no changes needed in loop logic)
        revision_count = 0
        while revision_count < MAX_REVISIONS:
            feedback = self._get_user_feedback(current_campaign)

            if feedback is None: # User approved
                logger.info(f"Campaign {current_campaign.campaign_id} for vendor '{current_campaign.vendor_name}' approved by user.")
                return current_campaign
            else: # User provided feedback
                revision_count += 1
                logger.info(f"Attempting revision {revision_count}/{MAX_REVISIONS} for vendor '{current_campaign.vendor_name}'...")
                revised_campaign = self.revise_campaign(current_campaign, feedback)

                if revised_campaign:
                    current_campaign = revised_campaign
                else:
                    logger.error("Failed to revise the campaign based on feedback. Showing last successful version.")
                    print("Sorry, there was an error applying the revisions. Please review the previous version again or provide different feedback.")
        
        # 3. Max revisions reached
        logger.warning(f"Maximum revision limit ({MAX_REVISIONS}) reached for vendor '{current_campaign.vendor_name}'.")
        print(f"\nMaximum revision attempts reached. Using the last generated version for vendor '{current_campaign.vendor_name}':")
        print(f"Campaign ID: {current_campaign.campaign_id}")
        final_confirm = input("Do you want to accept this last version? (yes/no): ").strip().lower()
        if final_confirm == 'yes':
             logger.info(f"User accepted the campaign for vendor '{current_campaign.vendor_name}' after max revisions.")
             return current_campaign
        else:
             logger.info(f"User did not accept the campaign for vendor '{current_campaign.vendor_name}' after max revisions.")
             return None


# --- Example Usage (human_in_loop.py) ---
if __name__ == "__main__":
    logger.info("Human-in-the-Loop Campaign Refinement Example (Extracting Vendor Name)")

    # --- Initialize Agent ---
    # ... (agent initialization remains the same) ...
    if not os.getenv("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY environment variable not set. Please set it to run the example.")
        agent = None
    else:
        try:
            # Use the updated agent
            agent = CampaignGenerationAgent()
        except Exception as e:
            logger.error(f"Failed to initialize CampaignGenerationAgent: {e}", exc_info=True)
            agent = None

    if not agent:
        logger.error("Agent could not be initialized. Exiting.")
        exit()

    # --- Initialize HITL Manager ---
    hitl_manager = HumanInLoopManager(agent)

    # # --- Get Input from User (only file path needed) ---
    # print("Please provide the following details:")
    # while True:
    #     file_path = input("Enter the full path to the catalog file (e.g., /path/to/catalog.png): ").strip()
    #     if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    #         break
    #     # ... (file validation remains the same) ...
    #     elif not os.path.exists(file_path):
    #          print(f"Error: File not found at '{file_path}'. Please check the path and try again.")
    #     else:
    #          print(f"Error: File '{file_path}' is empty. Please provide a valid catalog file.")

    # Removed vendor_name input
    # logger.info(f"User provided catalog path: {file_path}")

    # --- Define Data Folder (for saving output) ---
    data_folder = "/Users/1arijits/PROFESSIONAL/RevPointsPlus/data"
    # Using the same test file as before
    vendor = "HG Breakfast Menu"
    file_path = os.path.join(data_folder, "hg_Breakfast2024_Hand_Menu_ENG_Web_Option_02_583b27cb3f.png")

    # --- Run HITL Process ---
    # Call run_interaction without vendor_name
    final_campaign = hitl_manager.run_interaction(catalog_file_path=file_path)

    if final_campaign:
        # Vendor name comes from the final_campaign object
        logger.info(f"HITL process complete. Final approved campaign for vendor: '{final_campaign.vendor_name}'")
        print("\n--- Final Approved Campaign ---")
        print(f"Campaign ID: {final_campaign.campaign_id}")
        print(f"Timestamp: {final_campaign.timestamp}")
        print(f"Vendor: {final_campaign.vendor_name}") # Display extracted/final vendor name
        # ... (rest of printing) ...
        print("-----------------------------")

        # Save the final approved campaign
        campaign_folder = os.path.join(data_folder, "campaigns_approved")
        if not os.path.exists(campaign_folder):
            try:
                os.makedirs(campaign_folder)
                logger.info(f"Created directory for approved campaigns: {campaign_folder}")
            except OSError as e:
                logger.error(f"Failed to create directory {campaign_folder}: {e}")

        if os.path.exists(campaign_folder):
            # Use extracted/final vendor name in filename
            safe_vendor_name = "".join(c if c.isalnum() else "_" for c in final_campaign.vendor_name)
            json_file_path = os.path.join(campaign_folder, f"{safe_vendor_name}_{final_campaign.campaign_id}_approved.json")
            try:
                with open(json_file_path, "w") as json_file:
                    json_file.write(final_campaign.model_dump_json(indent=4))
                print(f"Final approved campaign saved to {json_file_path}")
                logger.info(f"Final approved campaign saved to {json_file_path}")
            except IOError as e:
                 logger.error(f"Failed to save approved campaign to {json_file_path}: {e}")
        else:
            logger.error(f"Output directory {campaign_folder} does not exist. Cannot save campaign.")

    else:
        logger.info(f"HITL process for catalog '{os.path.basename(file_path)}' concluded without an approved campaign.")
        print("\n--- Campaign generation process aborted or no campaign was approved. ---")