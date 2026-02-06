from ..tools.scraper import fetch_country_infobox
from ..tools.database import save_country_data, get_country_data

# 1. Fetch live data from Wikipedia
country = "France"
print(f"🌐 Fetching data for {country}...")
info = fetch_country_infobox(country)

if info:
    # 2. Save it to your DB using the tool from Step 1
    save_country_data(country, info)
    
    # 3. Verify it's in the DB
    saved_data = get_country_data(country)
    print(f"✅ Successfully saved {country} to DB.")
    print(f"📍 Capital of {country}: {saved_data.get('Capital')}")
    print(f"💶 Currency of {country}: {saved_data.get('Currency')}")
