import sqlite3
import json
import re
from datetime import datetime

DB_PATH = "data/countries.db"


def canonicalize_key(key: str) -> str:
    key = key.lower()
    key = re.sub(r'\(.*?\)', '', key)
    key = re.sub(r'[^a-z0-9 ]', '', key)
    key = re.sub(r'\s+', '_', key)
    return key.strip('_')


def clean_value(value: str) -> str:
    value = re.sub(r'\[.*?\]', '', value)
    value = re.sub(r'\d+°.*?[NSEW]', '', value)
    value = re.sub(r'\s+', ' ', value)
    return value.strip()


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, attributes FROM countries")
    rows = cursor.fetchall()

    print(f"🔄 Migrating {len(rows)} countries")

    for row_id, name, attributes in rows:
        try:
            raw_data = json.loads(attributes)
        except Exception:
            print(f"⚠️ Skipping {name} (invalid JSON)")
            continue

        cleaned = {}

        for k, v in raw_data.items():
            clean_k = canonicalize_key(k)
            clean_v = clean_value(v)

            if clean_k and clean_v:
                cleaned[clean_k] = clean_v

        cursor.execute(
            """
            UPDATE countries
            SET attributes = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                json.dumps(cleaned),
                datetime.utcnow(),
                row_id
            )
        )

        print(f"✅ Cleaned: {name}")

    conn.commit()
    conn.close()
    print("🎉 Migration complete")


if __name__ == "__main__":
    migrate()

