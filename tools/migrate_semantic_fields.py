import sqlite3
import json
from datetime import datetime

DB_PATH = "data/countries.db"

KEY_MAP = {
    "capital_and_largest_city": "capital",
    "official_language": "official_language",
    "government": "government",
    "monarch": "monarch",
    "prime_minister": "prime_minister",
    "currency": "currency",
    "calling_code": "calling_code",
    "internet_tld": "internet_tld",
    "total": "gdp_nominal",
    "per_capita": "gdp_per_capita",
    "2025_estimate": "population",
}

DROP_PREFIXES = (
    "kingdom_of_",
    "basque",
    "catalan",
    "galician",
    "occitan",
    "valencian",
)


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, attributes FROM countries")
    rows = cursor.fetchall()

    print(f"🧠 Semantic migration for {len(rows)} countries")

    for row_id, name, attributes in rows:
        raw = json.loads(attributes)
        clean = {}

        for k, v in raw.items():
            if k.startswith(DROP_PREFIXES):
                continue

            if k in KEY_MAP:
                clean[KEY_MAP[k]] = v

        cursor.execute(
            """
            UPDATE countries
            SET attributes = ?, updated_at = ?
            WHERE id = ?
            """,
            (json.dumps(clean), datetime.utcnow(), row_id)
        )

        print(f"✅ Normalized: {name}")

    conn.commit()
    conn.close()
    print("🎉 Semantic migration complete")


if __name__ == "__main__":
    migrate()

