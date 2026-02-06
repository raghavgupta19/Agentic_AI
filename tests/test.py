
from ..core.orchestrator import ask_agent
from ..tools.database import save_country_data

save_country_data("Germany", {
    "Capital": "Berlin",
    "Currency": "Euro"
})

answer, country = ask_agent("What is the capital of Germany?")
print(answer)
answer, country = ask_agent("What is its currency?", current_country=country)
print(answer)
answer, country = ask_agent("What is the capital of Nepal?")
print(answer)

