from ..tools.scraper import fetch_country_infobox
from ..tools.cleaner import manual_scrub
from ..core.orchestrator import ask_agent
raw = fetch_country_infobox("Nepal")
clean = manual_scrub(raw)

print(clean["Capital"])
print(clean["Prime Minister"])
print(clean["Currency"])
answer, country = ask_agent("Who is the prime minister of Nepal?")
print(answer)

answer, country = ask_agent("What is the currency?", country)
print(answer)
