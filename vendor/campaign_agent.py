import os
import json
import uuid
import traceback
import logging
import datetime
import base64
import mimetypes
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ValidationError, field_validator
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers.openai_functions import JsonOutputFunctionsParser
# Corrected import based on the error message
from langchain_core.output_parsers import JsonOutputKeyToolsParser
from langchain_core.pydantic_v1 import Field as V1Field # For function calling schema with Langchain + Gemini
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function
from tqdm import tqdm
import time
import dotenv

# --- Load Environment Variables ---    
dotenv.load_dotenv()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("campaign_agent.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
# Use Pydantic V1 Field for compatibility with Langchain's function calling conversion
class CampaignFormatBase(BaseModel):
    """Pydantic model for the structured output of the campaign generation, used for function calling."""
    vendor_name: str = Field(..., description="The name of the business or vendor identified from the catalog content.") 
    category: str = Field(..., description="The category or type of business, indicating its focus area, it should be strictly one of this - ['Restaurants', 'Groceries', 'Shopping', 'Travel and Transportation', 'Entertainment'].")
    promotions: List[str] = Field(..., description="A list of specific promotional offers based on the catalog. Each promotion MUST be phrased in terms of points, like 'Use 500 points for 10% off Product X' or 'Use 1000 points for €15 off your total order'. Be creative and relevant to the catalog content.")
    notification: str = Field(..., description="Compelling notification text (max 150 chars). It should create urgency or FOMO (Fear Of Missing Out), hint at the promotions and the slogan, and entice users to click. Example: '⏳ Don't miss out! Use points for HUGE savings, spend xx points to save xx eur on your next purchase at [Vendor Name] this week only! Tap to see deals.'")
    campaign_message: str = Field(..., description="The main message of the campaign aimed at engaging potential customers, explaining the value proposition and highlighting key offers from the catalog. Use emojis to enhance engagement.")
    campaign_slogan: str = Field(..., description="A catchy slogan (max 10 words) that encapsulates the campaign's key selling point or theme derived from the catalog. Use emojis to enhance engagement.")

class CampaignFormat(CampaignFormatBase):
    """Final campaign format including metadata."""
    campaign_id: str = Field(..., description="A unique identifier for the campaign.")
    timestamp: datetime.datetime = Field(..., description="The date and time when the campaign was generated.")

    @field_validator('timestamp', mode='before')
    def set_timestamp(cls, v):
        return v or datetime.datetime.now()

    @field_validator('campaign_id', mode='before')
    def set_campaign_id(cls, v):
        return v or str(uuid.uuid4())


# --- Campaign Generation Agent ---
class CampaignGenerationAgent:
    """
    Agent that generates marketing campaigns for businesses based on their catalogs (JPG/PDF)
    using Google Gemini Pro Vision API and logs the process.
    """
    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the agent with the Google API key.

        Args:
            api_key: The Google API key. Reads from GOOGLE_API_KEY environment variable if None.
        """
        logger.info("Initializing CampaignGenerationAgent...")
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.error("Google API Key not provided or found in environment variables.")
            raise ValueError("Google API Key is required.")

        try:
            # Using a model that supports function calling and vision like gemini-1.5-pro-latest
            # Adjust model name if necessary based on availability and specific needs
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-pro-exp-03-25",
                google_api_key=self.api_key,
                temperature=0.7, # Add some creativity
                convert_system_message_to_human=True # Often needed for Gemini function calling
            )
            logger.info(f"Initialized Gemini LLM with model: {self.llm.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini LLM: {e}", exc_info=True)
            raise

        # Prepare the function definition for the LLM using the updated CampaignFormatBase
        self.output_function = convert_pydantic_to_openai_function(CampaignFormatBase)
        self.llm_with_tools = self.llm.bind_tools(
            [CampaignFormatBase],
            tool_choice=self.output_function['name']
        )
        self.output_parser = JsonOutputKeyToolsParser(
                key_name=self.output_function['name'],
                first_tool_only=True
            )
        logger.info("LLM bound with output function (including vendor_name extraction) and parser configured.")

    def _encode_file(self, file_path: str) -> tuple[Optional[str], Optional[str]]:
        # ... (Encoding function remains the same) ...
        try:
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type or not (mime_type.startswith("image/") or mime_type == "application/pdf"):
                logger.error(f"Unsupported file type: {mime_type} for file: {file_path}")
                return None, None

            with open(file_path, "rb") as f:
                encoded_content = base64.b64encode(f.read()).decode("utf-8")
            logger.info(f"Successfully encoded file: {file_path} (MIME type: {mime_type})")
            return encoded_content, mime_type
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None, None
        except Exception as e:
            logger.error(f"Error encoding file {file_path}: {e}", exc_info=True)
            return None, None

    def _create_prompt_messages(self, encoded_content: str, mime_type: str) -> List[Any]: # Removed vendor_name parameter
        """Creates the list of messages for the LLM prompt, asking it to extract vendor name."""
        system_prompt = f"""
            You are a creative marketing assistant for a payment platform. Your task is to analyze the provided business catalog (image or PDF) and generate a compelling marketing campaign.

            Follow these instructions STRICTLY:
            1.  Analyze the catalog content (products, services, prices, style).
            2.  **Identify the Vendor Name:** Determine the name of the business or vendor from the catalog content itself. Include this identified name in the `vendor_name` field of your JSON output.
            3.  Generate campaign details based *only* on the catalog provided.
            4.  **Promotions:** Create a list of 2-4 specific, attractive promotions involving points (e.g., "Use 500 points for 10% off X"). Make them relevant to the catalog.
            5.  **Notification:** Craft a short (max 150 chars), urgent notification mentioning the **identified vendor name** and points savings.
            6.  **Campaign Message:** Write an engaging message highlighting offers, mentioning the **identified vendor name**.
            7.  **Campaign Slogan:** Create a short, catchy slogan (max 10 words) for the identified vendor.
            8.  **Category:** Assign ONE category strictly from: ['Restaurants', 'Groceries', 'Shopping', 'Travel and Transportation', 'Entertainment'].
            9.  Output the results ONLY in the requested JSON format using the provided function call schema, ensuring the `vendor_name` field contains the name you identified. Do not add extra text.
            """

        human_message_content = [
            {"type": "text", "text": "Generate a marketing campaign based on the following catalog. Please identify the vendor name from the catalog content and include it in your response."}, # Updated text
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{encoded_content}"
                }
            }
        ]

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message_content)
        ]
        logger.debug("Generated prompt messages asking LLM to extract vendor name.")
        return messages

    def generate_campaign(self, catalog_file_path: str) -> Optional[CampaignFormat]: # Removed vendor_name parameter
        """
        Generates a marketing campaign from a catalog file, attempting to extract the vendor name.

        Args:
            catalog_file_path: Path to the JPG, PNG, or PDF catalog file.

        Returns:
            A CampaignFormat object containing the generated campaign details (including extracted vendor name),
            or None if an error occurs.
        """
        logger.info(f"Starting campaign generation using catalog: {catalog_file_path} (attempting vendor name extraction)") # Updated log

        if not os.path.exists(catalog_file_path):
            logger.error(f"Catalog file not found: {catalog_file_path}")
            return None

        encoded_content, mime_type = self._encode_file(catalog_file_path)
        if not encoded_content or not mime_type:
            logger.error("Failed to encode catalog file.")
            return None

        prompt_messages = self._create_prompt_messages(encoded_content, mime_type) # Call without vendor_name

        try:
            logger.info("Invoking Gemini LLM to analyze catalog, extract vendor name, and generate campaign...") # Updated log
            start_time = time.time()
            chain = self.llm_with_tools | self.output_parser
            response = chain.invoke(prompt_messages)
            end_time = time.time()
            logger.info(f"LLM invocation completed in {end_time - start_time:.2f} seconds.")
            logger.debug(f"Raw LLM response (parsed function arguments): {response}")

            if not isinstance(response, dict):
                 logger.error(f"LLM response is not a dictionary: {type(response)} - {response}")
                 # Add fallback logic if needed
                 return None
            else:
                response_data = response

            # Validate and structure the final output
            # Vendor name is now expected within response_data from the LLM
            campaign_data = CampaignFormatBase(**response_data) # Validates base fields including vendor_name
            final_campaign = CampaignFormat(
                **campaign_data.dict(), # Use validated data (includes vendor_name)
                campaign_id=str(uuid.uuid4()),
                timestamp=datetime.datetime.now()
            )

            # Use the extracted vendor name in logging
            logger.info(f"Successfully generated and validated campaign: {final_campaign.campaign_id} for extracted vendor: '{final_campaign.vendor_name}'")
            logger.debug(f"Generated campaign details: {final_campaign.model_dump_json(indent=2)}")
            return final_campaign

        except ValidationError as e:
            failed_vendor = response.get('vendor_name', '[vendor name extraction failed]') if isinstance(response, dict) else '[vendor name extraction failed]'
            logger.error(f"Pydantic validation error for extracted vendor '{failed_vendor}': {e}", exc_info=True)
            logger.error(f"LLM Response that failed validation: {response}")
            return None
        except Exception as e:
            failed_vendor = response.get('vendor_name', '[vendor name extraction failed]') if isinstance(response, dict) else '[vendor name extraction failed]'
            logger.error(f"An error occurred during campaign generation for extracted vendor '{failed_vendor}': {e}", exc_info=True)
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

# --- Example Usage ---
if __name__ == "__main__":
    logger.info("Campaign Agent Example Usage")

    # IMPORTANT: Set your Google API Key as an environment variable
    # export GOOGLE_API_KEY='your_api_key_here'
    # Or pass it directly: CampaignGenerationAgent(api_key='your_api_key_here')
    if not os.getenv("GOOGLE_API_KEY"):
        logger.warning("GOOGLE_API_KEY environment variable not set. Please set it to run the example.")
        # Example: agent = CampaignGenerationAgent(api_key="YOUR_API_KEY")
        agent = None # Avoids running without key
    else:
         agent = CampaignGenerationAgent()


    # --- Define Test Cases ---
    # Use absolute paths or paths relative to where the script is run
    data_folder = "/Users/1arijits/PROFESSIONAL/RevPointsPlus/data"
    test_files = [ # Just a list of file paths
        os.path.join(data_folder, "hg_Breakfast2024_Hand_Menu_ENG_Web_Option_02_583b27cb3f.png"),
        # Add more catalog file paths here if needed
    ]

    # --- Run Campaign Generation ---
    if agent:
        for vendor, file_path in test_files.items():
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0: # Check if file exists and is not empty
                print("-" * 30)
                logger.info(f"--- Generating campaign for: {os.path.basename(file_path)} ---")
                campaign = agent.generate_campaign(catalog_file_path=file_path)
                logger.info(f"--- Campaign generation completed for : {campaign} ---")

                if campaign:
                    print("\n--- Generated Campaign ---")
                    print(f"Campaign ID: {campaign.campaign_id}")
                    print(f"Timestamp: {campaign.timestamp}")
                    print(f"Vendor: {campaign.vendor_name}")
                    print(f"Category: {campaign.category}")
                    print("Promotions:")
                    for promo in campaign.promotions:
                        print(f"  - {promo}")
                    print(f"Notification: {campaign.notification}")
                    print(f"Slogan: {campaign.campaign_slogan}")
                    print(f"Message: {campaign.campaign_message}")
                    print("--------------------------\n")
                    
                    # Save the campaign output as a JSON file in the data_folder
                    campaign_folder = os.path.join(data_folder, "campaigns")
                    if not os.path.exists(campaign_folder):
                        os.makedirs(campaign_folder)
                    json_file_path = os.path.join(campaign_folder, f"{campaign.campaign_id}.json")
                    with open(json_file_path, "w") as json_file:
                        json_file.write(campaign.model_dump_json(indent=4))
                    print(f"Campaign saved to {json_file_path}")
                else:
                    print(f"\n--- Failed to generate campaign for {os.path.basename(file_path)} ---")
                    print("--------------------------\n")
            elif not os.path.exists(file_path):
                 logger.error(f"Skipping vendor '{vendor}'. Catalog file '{file_path}' not found.")
            else:
                 logger.error(f"Skipping vendor '{vendor}'. Catalog file '{file_path}' is empty. Please provide a real catalog.")
                 print(f"Skipping vendor '{vendor}'. Catalog file '{file_path}' is empty. Please provide a real catalog.")
    else:
        logger.error("Agent could not be initialized. Please check your API key configuration.")
