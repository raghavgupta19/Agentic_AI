# orchestrator.py
import os
import json
import time
import re
from google import genai
from google.genai import errors
from dotenv import load_dotenv

from tools.database import get_country_data, save_country_data, get_from_graph
from tools.scraper import fetch_country_infobox
from tools.cleaner import clean_scraped_data, manual_scrub

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-2.0-flash"

# ---------- LLM WRAPPER ----------
def call_gemini_with_retry(prompt, retries=3, delay=15):
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            return response.text
        except errors.ClientError as e:
            if "429" in str(e) and i < retries - 1:
                time.sleep(delay)
                continue
            raise e
    return None

# ---------- FUZZY ATTRIBUTE MATCH ----------
def find_best_attribute_match(target_attr, data_dict):
    target_attr = target_attr.lower().replace(" ", "")
    for key, val in data_dict.items():
        key_norm = key.lower().replace(" ", "")
        if target_attr in key_norm or key_norm in target_attr:
            return val
    return None

# ---------- MAIN AGENT ----------
def ask_agent(user_query, current_country=None):
    query = user_query.lower()
    target_country = None
    target_attr = None

    # ---------- STEP 1: RULE-BASED ----------
    patterns = [
        r"(?P<attr>capital|population|currency|leader|president|pm|religion|official languages)\s+of\s+(?P<country>[a-zA-Z\s]+)",
        r"(?P<country>[a-zA-Z\s]+)'s\s+(?P<attr>capital|population|currency|leader|president|pm|religion|official languages)"
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            target_country = match.group("country").strip().title()
            target_attr = match.group("attr").strip().title()
            break

    # ---------- STEP 2: CONTEXT FALLBACK ----------
    if not target_country and current_country:
        target_country = current_country
        for attr in ["capital", "population", "currency", "leader", "president", "pm", "religion", "official languages"]:
            if attr in query:
                target_attr = attr.title()
                break

    # ---------- STEP 3: DB / SCRAPER ----------
    data = get_country_data(target_country)
    if not data:
        raw = fetch_country_infobox(target_country)
        if not raw:
            return f"No data found for {target_country}.", None
        try:
            data = clean_scraped_data(raw)
        except:
            data = manual_scrub(raw)
        save_country_data(target_country, data)

    # ---------- STEP 4: GRAPH ----------
    graph_fact = get_from_graph(target_country, target_attr)
    if graph_fact:
        return f"The {target_attr} of {target_country} is {graph_fact}.", target_country

    # ---------- STEP 5: ATTRIBUTE MATCH ----------
    fact = find_best_attribute_match(target_attr, data)
    if fact:
        return f"The {target_attr} of {target_country} is {fact}.", target_country

    # ---------- STEP 6: LLM SYNTHESIS (IF NEEDED) ----------
    synthesis_prompt = f"Using this data {json.dumps(data)}, answer: {user_query}"
    try:
        answer = call_gemini_with_retry(synthesis_prompt)
        return answer.strip(), target_country
    except:
        return f"I have data for {target_country}, but not that detail.", target_country
