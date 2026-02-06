# Country Information Agent

A Streamlit-based application that retrieves and displays country information from Wikipedia using web scraping and graph-based data management.

## Features

- Scrape country information from Wikipedia
- Store data in SQLite database
- Query country attributes (capital, currency, PM, etc.)
- Visualize country data relationships as interactive graphs
- Support for multiple countries

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Internet connection (for Wikipedia scraping)

## Installation

1. Clone the repository:
```bash
cd /home/raghavgupta/country-agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Create .env file with your Gemini API key (optional)
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

### Query Examples

- "pm of India" → Returns Prime Minister
- "capital of India" → Returns Capital city
- "currency of India" → Returns Currency
- "official languages of India" → Returns Official languages

Click "Show Graph" button to visualize country data relationships.

## Project Structure

```
country-agent/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .env                   # Environment configuration
├── core/
│   └── orchestrator.py    # Core application logic
├── tools/
│   ├── scraper.py        # Wikipedia scraping module
│   ├── database.py       # Database and graph operations
│   └── cleaner.py        # Data cleaning utilities
└── data/
    └── countries.db      # SQLite database
```

## Technical Details

- **Data Source**: Wikipedia country infoboxes
- **Database**: SQLite
- **Graph**: NetworkX for relationship mapping
- **Visualization**: HoloViews + Bokeh
- **Frontend**: Streamlit

## Notes

- First query for a country will scrape and cache data
- Subsequent queries use cached database data
- Graph visualization shows country attributes and relationships
