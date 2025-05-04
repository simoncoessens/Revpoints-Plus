import os
import json
import argparse
import re
import datetime
from openai import OpenAI

# ─────────────── Configuration ───────────────

# --- Perplexity API ---
# Consider using environment variables for security in production
# export PERPLEXITY_API_KEY="your_pplx_key_here"
# API_KEY = os.getenv("PERPLEXITY_API_KEY")
API_KEY = "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" # Hardcoded as per your example
if not API_KEY:
    raise RuntimeError("Please set your PERPLEXITY_API_KEY or hardcode it")

# Initialize the Perplexity client
try:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.perplexity.ai",
    )
except Exception as e:
    print(f"Error initializing Perplexity client: {e}")
    exit(1)


# --- Email Template ---
TEMPLATE_FILENAME = 'contact_template.eml'
OUTPUT_DIR = 'generated_vendor_emails'

# --- Predefined Data for Template (Customize as needed) ---
# You might fetch this dynamically or have different sets per vendor type
PREDEFINED_DATA = {
    "contact_name_fallback": "Business Owner/Manager", # Used if specific name not found
    "avg_transaction": "€28.75",
    "nearby_customers": "~4,200+",
    "category": "General Retail / Local Services",
    "verify_link_base": "https://business.revolut.com/partner-verify", # Example
    "unsubscribe_link_base": "https://business.revolut.com/unsubscribe", # Example
    "image_url": "https://i.imgur.com/yourImageID.png" # <-- !!! REPLACE WITH YOUR ONLINE IMAGE URL !!!
}

# ─────────────── Perplexity Prompt Templates ───────────────
SYSTEM_PROMPT = (
    "You are an AI assistant specialized in finding business contact information. "
    "When given a store name and location, you MUST focus on finding the primary contact email address and a telephone number. "
    "Return ONLY a valid JSON object with the keys `email`, `telephone`, and `sources`. "
    "The `email` value should be a string or null if not found. "
    "The `telephone` value should be a string or null if not found. "
    "The `sources` field should be a list of {\"url\":…, \"snippet\":…} objects "
    "showing where you found the information. Provide at least 2-3 sources if possible. "
    "Do not include any introductory text, greetings, apologies, or explanations outside the JSON structure. "
    "If you cannot find an email, return null for the email field."
    # Removed the _debug request to simplify parsing
)

USER_PROMPT = (
    "Store Name: {store}\n"
    "Location: {location}\n\n"
    "Find the primary contact email and telephone for this business. Provide sources. Respond ONLY with the JSON object."
)

# ─────────────── Core Functions ───────────────

def get_vendor_contact(store_name: str, store_location: str, stream_output: bool = True):
    """Uses Perplexity API to find vendor contact info."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_PROMPT.format(store=store_name, location=store_location),
        },
    ]

    print(f"🔍 Searching for contact info for '{store_name}' in '{store_location}' using Perplexity...")
    try:
        resp = client.chat.completions.create(
            model="sonar-pro", 
            messages=messages,
            stream=stream_output, # Keep streaming for user feedback
        )
    except Exception as e:
        print(f"\n❌ Error calling Perplexity API: {e}")
        return None

    full_response = ""
    if stream_output:
        print("⏳ Thinking...", end="", flush=True)
        try:
            for chunk in resp:
                delta_obj = chunk.choices[0].delta
                delta = delta_obj.content if hasattr(delta_obj, "content") and delta_obj.content else ""
                print(delta, end="", flush=True)
                full_response += delta
            print() # Newline after stream
        except Exception as e:
             print(f"\n❌ Error processing stream from Perplexity API: {e}")
             return None
    else:
        try:
            full_response = resp.choices[0].message.content
            print(full_response)
        except Exception as e:
             print(f"\n❌ Error getting response from Perplexity API: {e}")
             return None


    # --- Enhanced JSON Parsing ---
    # Try to find JSON block even if there's surrounding text (though prompt asks not to)
    json_match = re.search(r'\{.*\}', full_response, re.DOTALL)
    if not json_match:
        print("\n⚠️ Warning: No JSON object found in the response.")
        print("Raw Output:\n---\n", full_response, "\n---")
        return None

    json_str = json_match.group(0)
    data = json.loads(json_str)
    # Basic validation
    if not isinstance(data, dict):
            raise ValueError("Parsed data is not a dictionary.")
    print("\n✅ Successfully parsed JSON from response.")
    return data


def populate_and_save_email(template_content: str, vendor_email: str, vendor_name: str, predefined: dict):
    """Populates the email template and saves it to a file."""
    content = template_content
    current_year = str(datetime.datetime.now().year)

    # --- Generate Dynamic Data ---
    # Simple example: add email to unsubscribe link query param
    unsubscribe_link = f"{predefined['unsubscribe_link_base']}?email={vendor_email}"
    # Simple example: add vendor name to verify link query param (URL-encoded if needed)
    verify_link = f"{predefined['verify_link_base']}?vendor={vendor_name.replace(' ', '%20')}"

        # --- Perform Replacements ---
    print(f"🔧 Populating template for {vendor_name} ({vendor_email})...")

    # 1. Handle simple text replacements using direct string replacement
    literal_replacements = {
        # Use the literal placeholder strings as keys
        '[Vendor Email]': vendor_email, # Placeholder for email address if needed in body
        '[Vendor Contact Name]': vendor_name,
        'unique_vendor_name': vendor_name,
        'unique_avg_transaction': predefined['avg_transaction'],
        'unique_nearby': predefined['nearby_customers'],
        '[Spending Category]': predefined['category'],
        '[Verification Link]': verify_link,
        '[Unsubscribe Link]': unsubscribe_link,
        '[Current Year]': current_year,
    }

    for placeholder, value in literal_replacements.items():
         # Use standard string replace - less prone to regex/encoding issues for simple tags
         content = content.replace(placeholder, value)
         # Add a check to see if replacement happened (for debugging)
         # if placeholder in content:
         #     print(f"  ⚠️ Placeholder '{placeholder}' might still be present after replacement attempt.")
         # else:
         #     print(f"  ✅ Replaced '{placeholder}'")


    # 2. Handle image replacement using regex (more complex structure)
    try:
        # Make sure the image URL is valid before attempting replacement
        if predefined.get("image_url"):
            # This regex finds an img tag with the specific style and replaces its src
            # It assumes the template initially has *some* src attribute to replace.
            image_pattern = re.compile(
                r'(<img[^>]*?)src=3D"[^"]*"([^>]*?style=3D"border:0;display:block[^>]*>)' ,
                re.IGNORECASE | re.DOTALL
            )
            image_replacement_string = rf'\1src=3D"{predefined["image_url"]}"\2'

            # Check if the pattern exists before trying to replace
            if image_pattern.search(content):
                content = image_pattern.sub(image_replacement_string, content)
                print(f"  ✅ Updated image src to: {predefined['image_url']}")
            else:
                print("  ⚠️ Image tag pattern not found for replacement.")
        else:
            print("  ⚠️ No image_url defined in PREDEFINED_DATA.")

    except Exception as e:
        print(f"  ❌ Error during image replacement: {e}")


    # --- Explicitly Update 'To:' Header ---
    # This ensures the main email header is correct, regardless of body placeholders
    # Use re.IGNORECASE just in case the header casing varies
    content = re.sub(r'^To:.*$', f"To: {vendor_email}", content, flags=re.MULTILINE | re.IGNORECASE)
    # Add a check for the To: header
    if not re.search(rf'^To: {re.escape(vendor_email)}', content, flags=re.MULTILINE | re.IGNORECASE):
        print("  ⚠️ Failed to update 'To:' header correctly.")
    else:
        print("  ✅ Updated 'To:' header.")

    # --- Save the Output ---
    # (Keep the saving logic as it was)
    # Create a safe filename
    safe_vendor_name = re.sub(r'[^\w\-]+', '_', vendor_name)
    output_filename = os.path.join(OUTPUT_DIR, f"Revolut_Outreach_{safe_vendor_name}_{vendor_email}.eml")

    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True) # Create dir if needed
        with open(output_filename, 'w', encoding='utf-8', newline='\r\n') as f: # Use CRLF for .eml
            f.write(content)
        print(f"✅ Successfully generated email: {output_filename}")
        return True
    except Exception as e:
        print(f"❌ Error writing output file '{output_filename}': {e}")
        return False


# ─────────────── CLI Entrypoint ───────────────
def main():
    parser = argparse.ArgumentParser(
        description="Lookup vendor contact info via Perplexity and generate a Revolut outreach email."
    )
    parser.add_argument("store", help="Name of the store/vendor to look up")
    parser.add_argument("location", help="Location (city, address, etc.) of the store")
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming Perplexity output (shows raw reasoning potentially)",
    )
    args = parser.parse_args()

    # --- Step 1: Get Vendor Contact Info ---
    vendor_data = get_vendor_contact(args.store, args.location, stream_output=not args.no_stream)

    if not vendor_data:
        print("❌ Could not retrieve or parse vendor data from Perplexity. Exiting.")
        return

    # --- Step 2: Extract Email (Crucial Step) ---
    vendor_email = vendor_data.get('email')
    vendor_phone = vendor_data.get('telephone') # Optional: could use later

    if not vendor_email or '@' not in vendor_email:
        print(f"❌ No valid email address found for '{args.store}' in the Perplexity response.")
        print("Raw vendor data found:", json.dumps(vendor_data, indent=2))
        return

    print(f"ℹ️ Found Email: {vendor_email}" + (f", Phone: {vendor_phone}" if vendor_phone else ""))


    # --- Step 3: Read Email Template ---
    try:
        with open(TEMPLATE_FILENAME, 'r', encoding='utf-8') as f:
            template_content = f.read()
        print(f"📄 Successfully read template file: {TEMPLATE_FILENAME}")
    except FileNotFoundError:
        print(f"❌ Error: Template file not found at '{TEMPLATE_FILENAME}'. Exiting.")
        return
    except Exception as e:
        print(f"❌ Error reading template file: {e}. Exiting.")
        return

    # --- Step 4: Populate and Save ---
    populate_and_save_email(
        template_content=template_content,
        vendor_email=vendor_email,
        vendor_name=args.store, # Use the input store name
        predefined=PREDEFINED_DATA
    )

if __name__ == "__main__":
    main()