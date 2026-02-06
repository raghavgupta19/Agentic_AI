from ..tools.database import init_db, save_country_data, get_country_data

# Initialize the DB
init_db()

# Test Saving (Simulating a scraper result)
sample_info = {"Capital": "New Delhi", "Currency": "Rupee", "Population": "1.4 Billion"}
save_country_data("India", sample_info)

# Test Retrieval
data = get_country_data("India")
print(f"Retrieved Capital: {data['Capital']}")
