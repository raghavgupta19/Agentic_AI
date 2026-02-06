import requests
from bs4 import BeautifulSoup
import re
import json

def canonicalize_key(key: str) -> str:
    """Clean key to remove spaces, brackets, special chars"""
    key = key.lower()
    key = re.sub(r'\(.*?\)', '', key)
    key = re.sub(r'\[.*?\]', '', key)
    key = re.sub(r'[^a-z0-9 ]', '', key)
    key = re.sub(r'\s+', '_', key)
    return key.strip('_')

def clean_value(value: str) -> str:
    """Clean values: remove brackets, ranks, coordinates, extra spaces"""
    value = re.sub(r'\[.*?\]', '', value)          # remove citations
    value = re.sub(r'\([^)]*rank[^)]*\)', '', value, flags=re.I)
    value = re.sub(r'\([^)]*\)', '', value)        # remove (12th), etc.
    value = re.sub(r'\d+°.*?[NSEW]', '', value)    # coordinates
    value = re.sub(r'\s+', ' ', value).strip()
    return value

def normalize_numbers(data: dict) -> dict:
    def clean_number(val):
        if not val:
            return None
        val = re.sub(r'[^\d]', '', val)  # remove all non-digit chars
        return int(val) if val else None
    for k in data:
        if any(x in k for x in ["population", "gdp", "per_capita", "density", "area"]):
            data[k] = clean_number(data[k])
    return data


def fetch_country_infobox(country_name: str) -> dict | None:
    """Scrape Wikipedia infobox and return ALL cleaned fields"""
    url = f"https://en.wikipedia.org/wiki/{country_name.replace(' ', '_')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"❌ Page not found: {country_name}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        infobox = soup.find("table", class_=re.compile("infobox"))

        if not infobox:
            print(f"❌ No infobox found for {country_name}")
            return None

        raw = {}
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if not th or not td:
                continue
            raw_key = " ".join(th.stripped_strings)
            raw_val = " ".join(td.stripped_strings)
            if raw_key and raw_val:
                raw[raw_key] = raw_val

        # CLEAN ALL FIELDS
        cleaned = {}
        for k, v in raw.items():
            ck = canonicalize_key(k)
            cv = clean_value(v)
            if cv:
                cleaned[ck] = cv

        # Normalize numeric fields
        cleaned = normalize_numbers(cleaned)

        # DEBUG
        print(f"✅ Scraped and cleaned {country_name}: {list(cleaned.keys())}")
        return cleaned

    except Exception as e:
        print(f"❌ Scraper error for {country_name}: {e}")
        return None

