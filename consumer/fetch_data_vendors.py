import os
import json
import argparse
import re
import requests
from urllib.parse import quote_plus
from openai import OpenAI
from tqdm import tqdm   # ← progress bar

# ─────────────── Configuration ───────────────
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY", "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")
if not PERPLEXITY_API_KEY:
    raise RuntimeError("Please set your PERPLEXITY_API_KEY environment variable")

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "48341946-7f8ff43596cf2384ad9e1d67a")
if not PIXABAY_API_KEY:
    raise RuntimeError("Please set your PIXABAY_API_KEY environment variable")

client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai",
)

SYSTEM_PROMPT_DETAILS = (
    "You are a data-enrichment assistant.\n"
    "Given a vendor name and location, provide:\n"
    "1. A brief 'About' summary (1–2 sentences).\n"
    "2. The official website URL.\n"
    "Return only a JSON object with keys 'about' and 'url'."
)
USER_PROMPT = "Vendor Name: {vendor}\nLocation: {location}\n\nRespond ONLY with valid JSON."


def _chat(system_prompt: str, user_prompt: str, stream: bool = False) -> str:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": user_prompt},
    ]
    resp = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
        stream=stream,
    )

    raw = ""
    if stream:
        for chunk in resp:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                print(delta.content, end="", flush=True)
                raw += delta.content
        print()
    else:
        raw = resp.choices[0].message.content

    # Strip markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw).strip()
    return raw


def _parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse JSON: {raw}")


def enrich_vendor_details(vendor: str, location: str, stream: bool = False) -> dict:
    raw = _chat(
        SYSTEM_PROMPT_DETAILS,
        USER_PROMPT.format(vendor=vendor, location=location),
        stream
    )
    return _parse_json(raw)


def fetch_vendor_logo(vendor: str, category: str) -> str:
    """
    Search Pixabay using both vendor name and category to find a representative logo image.
    """
    query = quote_plus(f"{vendor} {category}")
    url = (
        f"https://pixabay.com/api/"
        f"?key={PIXABAY_API_KEY}"
        f"&q={query}"
        f"&image_type=photo"
        f"&per_page=3"
        f"&safesearch=true"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    hits = data.get("hits", [])
    if not hits:
        return ""
    return hits[0].get("largeImageURL") or hits[0].get("webformatURL", "")


def main(input_path: str, output_path: str, stream: bool):
    # Load input list
    with open(input_path, "r", encoding="utf-8") as f:
        vendors = json.load(f)

    # Process each entry with a progress bar
    for entry in tqdm(vendors, desc="Enriching vendors"):
        name     = entry.get("vendor_name", "")
        loc      = entry.get("location_hint", "")
        category = entry.get("category", "")  # new category field
        try:
            details  = enrich_vendor_details(name, loc, stream)
            logo_url = fetch_vendor_logo(name, category)

            entry["About"]     = details.get("about", "")
            entry["url"]       = details.get("url", "")
            entry["image_url"] = logo_url
        except Exception as e:
            print(f"⚠️  Error enriching {name} ({loc}): {e}")

        # Dynamically write out current state after each entry
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(vendors, f, indent=2, ensure_ascii=False)

    print(f"✅ Enriched data written to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Enrich vendor JSON with About, URL, and logo via Perplexity + Pixabay"
    )
    parser.add_argument("input",  help="Path to input JSON file")
    parser.add_argument("output", help="Path to output enriched JSON file")
    parser.add_argument("--stream", action="store_true", help="Show streaming output")
    args = parser.parse_args()
    main(args.input, args.output, args.stream)