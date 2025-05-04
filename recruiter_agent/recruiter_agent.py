import os
import json
import argparse
from openai import OpenAI

# ─────────────── Configuration ───────────────
# Make sure you’ve set your key in the environment:
#   export PERPLEXITY_API_KEY="INSERT API KEY HERE"
API_KEY =  "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"
if not API_KEY:
    raise RuntimeError("Please set your PERPLEXITY_API_KEY environment variable")

# Initialize the Perplexity client
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.perplexity.ai",
)

# ─────────────── Prompt Templates ───────────────
SYSTEM_PROMPT = (
    "You are an AI assistant.  "
    "When given a store name and location, you will look up the vendor’s contact info "
    "(email and telephone), and return a JSON object with keys "
    "`email`, `telephone`, and `sources`.  "
    "The `sources` field should be a list of {\"url\":…, \"snippet\":…} objects "
    "showing where you found each piece of information.  "
    "Also include in your response any intermediate reasoning steps as a `_debug` field. Search for a lot of sources and take your time"
)

USER_PROMPT = (
    "Store Name: {store}\n"
    "Location: {location}\n\n"
    "Please find the vendor’s contact email and telephone, and cite your sources."
)

# ─────────────── Core Function ───────────────
def get_vendor_contact(store_name: str, store_location: str, stream: bool = True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": USER_PROMPT.format(store=store_name, location=store_location),
        },
    ]

    resp = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
        stream=stream,
    )

    if stream:
        full_response = ""
        print("⏳ Fetching and reasoning...")
        for chunk in resp:
            # Fix: read .content attribute, not dict.get()
            delta_obj = chunk.choices[0].delta
            delta = delta_obj.content if hasattr(delta_obj, "content") else ""
            print(delta, end="", flush=True)
            full_response += delta
        print()  # newline after stream
    else:
        full_response = resp.choices[0].message["content"]
        print(full_response)

    # Try to parse JSON out of the model’s output
    data = json.loads(full_response)

    return data


# ─────────────── CLI Entrypoint ───────────────
def main():
    parser = argparse.ArgumentParser(
        description="Lookup vendor contact info via the Perplexity API"
    )
    parser.add_argument("store", help="Name of the store/vendor to look up")
    parser.add_argument("location", help="Location (city, address, etc.) of the store")
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming (print only final JSON)",
    )
    args = parser.parse_args()

    result = get_vendor_contact(args.store, args.location, stream=not args.no_stream)
    if result:
        print("\n✅ Parsed result:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
