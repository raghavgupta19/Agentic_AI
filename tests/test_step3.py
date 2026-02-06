from ..core.orchestrator import ask_agent

# Test 1: New Country (Will Scrape)
print("--- Test 1 ---")
answer, country = ask_agent("What is the capital of Germany?")
print(answer)

# Test 2: Follow-up (Uses Context)
print("\n--- Test 2 ---")
answer, country = ask_agent("What is its currency?", current_country=country)
print(answer)

# Test 3: Existing Country (Should be instant - No scraping)
print("\n--- Test 3 ---")
answer, country = ask_agent("Who is the president of France?")
print(answer)
