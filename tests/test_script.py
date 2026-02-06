from ..tools.database import save_country_data, get_country_data
from ..tools.scraper import fetch_country_infobox

# Example country
country_name = "India"

# Scrape Wikipedia
data = fetch_country_infobox(country_name)

# Save all fields to DB
save_country_data(country_name, data)

# Fetch back from DB
print(get_country_data(country_name))

