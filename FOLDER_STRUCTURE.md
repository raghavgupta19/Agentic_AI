# Project Folder Structure

```
country-agent/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables configuration
├── india_graph.html                # Generated HTML graph for India data
├── india_graph.png                 # Generated PNG graph for India data
├── FOLDER_STRUCTURE.md             # This file - project structure documentation
│
├── core/                           # Core application logic
│   └── orchestrator.py             # Main orchestrator/controller logic
│
├── tools/                          # Utility tools and modules
│   ├── scraper.py                  # Web scraping functionality
│   ├── cleaner.py                  # Data cleaning utilities
│   ├── database.py                 # Database operations and management
│   ├── init_db.py                  # Database initialization script
│   ├── migrate_clean_data.py       # Data migration for cleaning
│   ├── migrate_fix_broken_values.py # Migration to fix broken values
│   ├── migrate_semantic_fields.py  # Migration for semantic field updates
│   └── migrate_value_cleanup.py    # Migration for value cleanup
│
├── data/                           # Data storage
│   └── countries.db                # SQLite database file for country data
│
├── scripts/                        # Standalone utility scripts
│   ├── graph_population.py         # Population graph visualization
│   └── verify_graph.py             # Graph verification utility
│
└── tests/                          # Test suite
    ├── test.py                     # Main test file
    ├── test_models.py              # Tests for data models
    ├── test_step1.py               # Step 1 test suite
    ├── test_step2.py               # Step 2 test suite
    ├── test_step3.py               # Step 3 test suite
    ├── test_script.py              # Additional test script
    └── clean_test.py               # Data cleaning functionality tests
```

## Directory Descriptions

### Root Level
- **app.py** - Main application entry point containing application initialization and startup logic
- **requirements.txt** - Python package dependencies and versions
- **.env** - Environment configuration file (credentials, API keys, etc.)
- **india_graph.html** - Generated HTML visualization graph for India population data
- **india_graph.png** - Generated PNG image of India population graph

### /core
Core business logic and orchestration:
- **orchestrator.py** - Orchestrates workflows, manages data flow between components

### /tools
Reusable utility modules:
- **scraper.py** - Handles web scraping operations for data collection
- **cleaner.py** - Data validation and cleaning routines
- **database.py** - Database initialization, connections, and CRUD operations
- **init_db.py** - Database initialization and setup script
- **migrate_clean_data.py** - Database migration script for data cleaning
- **migrate_fix_broken_values.py** - Database migration script to fix broken/invalid values
- **migrate_semantic_fields.py** - Database migration script for semantic field updates
- **migrate_value_cleanup.py** - Database migration script for general value cleanup

### /data
Data persistence:
- **countries.db** - SQLite database storing country-related information

### /scripts
Standalone utility and analysis scripts:
- **graph_population.py** - Utility for visualizing and graphing population data
- **verify_graph.py** - Utility to verify and validate generated graphs

### /tests
Test suite and test files:
- **test.py** - Main test file with core test utilities
- **test_models.py** - Tests for data models
- **test_step1.py** - Step 1 test suite
- **test_step2.py** - Step 2 test suite
- **test_step3.py** - Step 3 test suite
- **test_script.py** - Additional test script for specific functionality
- **clean_test.py** - Data cleaning functionality tests
