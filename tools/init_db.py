import sqlite3

DB_PATH = "data/countries.db"

def init_db():
    """Create the countries table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            name TEXT PRIMARY KEY,
            attributes TEXT,
            updated_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized and table created (if not exists).")
