# cleaner.py
import re

KEY_NORMALIZATION = {
    "capital": ["capital", "capital and largest city", "capital_and_largest_city"],
    "currency": ["currency"],
    "prime minister": ["prime minister", "pm", "prime_minister"],
    "president": ["president"],
    "population": ["population", "estimate", "census", "total", "2023_estimate"],
    "official languages": ["official language", "officiallanguages", "coofficial_languages"],
    "religion": ["religion"],
    "demonyms": ["demonyms", "nationality"]
}

def normalize_key(raw_key):
    key = raw_key.lower().strip()
    for clean, variants in KEY_NORMALIZATION.items():
        for v in variants:
            if v in key:
                return clean.title()
    # fallback: replace underscores and spaces
    key = key.replace("_", " ").strip().title()
    return key

def clean_value(value):
    val = str(value)

    # Remove citations
    val = re.sub(r'\[.*?\]', '', val)

    # Remove coordinates
    val = re.sub(r'\d+(\.\d+)?°?[NS]?\s*\d+(\.\d+)?°?[EW]?.*', '', val)

    # Remove bracketed metadata
    val = re.sub(r'\(.*?\)', '', val)

    # Remove unicode junk
    val = val.encode("ascii", "ignore").decode()

    # Normalize spaces
    val = re.sub(r'\s+', ' ', val).strip()

    return val

def manual_scrub(raw_data):
    clean_dict = {}
    for key, value in raw_data.items():
        clean_key = normalize_key(key)
        clean_val = clean_value(value)
        if clean_key and clean_val:
            clean_dict[clean_key] = clean_val
    return clean_dict

def clean_scraped_data(raw_data_dict, client=None):
    return manual_scrub(raw_data_dict)
