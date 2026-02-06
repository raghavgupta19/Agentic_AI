import sqlite3
import json
import re

DB_PATH = "data/countries.db"

NUMERIC_FIELDS = {
    "gdp_nominal",
    "gdp_per_capita",
    "population",
    "calling_code",
    "internet_tld"
}

def is_broken(value: str) -> bool:
    # Clearly broken patterns
    if value in {"$", "+", ".", ". .", ". . ."}:
        return True

    # Dollar sign with no digits
    if value.startswith("$") and not re.search(r"\d", value):
        return True

    # Only symbols or commas
    if not re.search(r"[a-zA-Z0-9]", value):
        return True

    return False


def fix_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, attributes FROM countries")
    rows = cur.fetchall()

    for row_id, attr_json in rows:
        attrs = json.loads(attr_json)
        changed = False

        for key in list(attrs.keys()):
            if key in NUMERIC_FIELDS:
                value = attrs[key]
                if isinstance(value, str) and is_broken(value):
                    attrs[key] = "Unknown"
                    changed = True

        if changed:
            cur.execute(
                "UPDATE countries SET attributes = ? WHERE id = ?",
                (json.dumps(attrs), row_id)
            )

    conn.commit()
    conn.close()
    print("✅ Broken values fixed")


if __name__ == "__main__":
    fix_db()

