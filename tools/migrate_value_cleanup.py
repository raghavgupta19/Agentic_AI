import sqlite3
import json
import re
from datetime import datetime

DB_PATH = "data/countries.db"

def clean_value(value: str) -> str:
    # Remove BOM / invisible chars
    value = value.replace("\ufeff", "").strip()

    # Remove rankings like "(12th)"
    value = re.sub(r"\(\s*\d+(st|nd|rd|th)\s*\)", "", value)

    # Remove coordinates from capital
    if "/" in value:
        value = value.split("/")[0].strip()

    # Normalize currency like "Euro ( € ) ( EUR )"
    if "Euro" in value and "EUR" in value:
        value = "Euro (EUR)"

    # Normalize whitespace
    value = re.sub(r"\s+", " ", value).strip()

    return value


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, attributes FROM countries")
    rows = cursor.fetchall()

    print(f"🧹 Cleaning values for {len(rows)} countries")

    for row_id, attributes in rows:
        data = json.loads(attributes)
        cleaned = {}

        for k, v in data.items():
            if isinstance(v, str):
                cleaned[k] = clean_value(v)
            else:
                cleaned[k] = v

        cursor.execute(
            """
            UPDATE countries
            SET attributes = ?, updated_at = ?
            WHERE id = ?
            """,
            (json.dumps(cleaned), datetime.utcnow(), row_id)
        )

    conn.commit()
    conn.close()
    print("✅ Value cleanup completed")


if __name__ == "__main__":
    migrate()

