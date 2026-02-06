# database.py
import sqlite3
import json
import networkx as nx
import re
from datetime import datetime
import holoviews as hv
from holoviews import opts

hv.extension('bokeh')
DB_PATH = "data/countries.db"

# List of attributes we want to treat as multi-value
MULTI_VALUE_KEYS = [
    "officiallanguages",
    "official_languages",
    "recognised_regionallanguages",
    "recognised_regional_languages",
    "native_languages",
    "religion",
    "currency",
    "capital",
    "demonyms",
    "ethnicgroups"
]

# ------------------ DB INIT ------------------
def init_db():
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

# ------------------ SAVE ------------------
def save_country_data(country: str, data: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO countries (name, attributes, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(name)
        DO UPDATE SET
            attributes=excluded.attributes,
            updated_at=excluded.updated_at
    """, (country, json.dumps(data), datetime.utcnow()))
    conn.commit()
    conn.close()

# ------------------ READ ------------------
def get_country_data(country_name: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT attributes FROM countries WHERE LOWER(name)=LOWER(?)", (country_name,))
    row = cur.fetchone()
    conn.close()
    return json.loads(row[0]) if row else None

# ------------------ KEY NORMALIZATION ------------------
def normalize_graph_key(key: str) -> str:
    """Normalize scraped keys to standard names for graph"""
    key = key.lower()
    key = key.replace(" ", "").replace("-", "").replace("_and_", "_")
    mapping = {
        "officiallanguageandnationallanguage": "official_languages",
        "officiallanguages": "official_languages",
        "recognisedregionallanguages": "recognised_regional_languages",
        "native_languages": "native_languages",
        "capitalandlargestcity": "capital",
        "ethnicgroups": "demonyms",
        "ethnicity": "demonyms",
        "religion": "religion",
        "currency": "currency",
        "pm": "pm",
        "prime_minister": "pm",
        "primeministerofind": "pm",
        "president": "president",
        "calling_code": "calling_code",
        "callingcode": "calling_code"
    }
    return mapping.get(key, key)

# ------------------ BUILD GRAPH ------------------
def build_graph_from_db():
    G = nx.Graph()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, attributes FROM countries")
    for name, attrs_json in cur.fetchall():
        country_node = f"country:{name}"
        G.add_node(country_node, type="country", label=name)
        attrs = json.loads(attrs_json)
        for key, value in attrs.items():
            if not value:
                continue
            key_clean = normalize_graph_key(key)
            value_str = str(value).strip()
            if key_clean in MULTI_VALUE_KEYS:
                items = re.split(r',|;| and ', value_str)
                for item in items:
                    item = item.strip()
                    if item:
                        node_name = f"{name}:{key_clean}:{item.lower()}"
                        G.add_node(node_name, type="attribute", label=item)
                        G.add_edge(country_node, node_name, relation=key_clean)
            else:
                node_name = f"{name}:{key_clean}"
                G.add_node(node_name, type="attribute", label=value_str)
                G.add_edge(country_node, node_name, relation=key_clean)
    conn.close()
    return G

# ------------------ GET ATTRIBUTE FROM GRAPH ------------------
def get_from_graph(country: str, attribute: str):
    G = build_graph_from_db()
    cnode = f"country:{country}"
    attribute_norm = attribute.lower().replace(" ", "").replace("_", "")
    if cnode not in G:
        return None
    for neighbor in G.neighbors(cnode):
        rel = G.edges[cnode, neighbor]["relation"].lower().replace(" ", "").replace("_", "")
        lbl = str(G.nodes[neighbor]["label"]).lower().replace(" ", "").replace("_", "")
        # Improved fuzzy matching
        if (attribute_norm in rel or rel in attribute_norm or 
            attribute_norm in lbl or lbl in attribute_norm):
            return G.nodes[neighbor]["label"]
    return None

# ------------------ COUNTRY SUBGRAPH ------------------
def build_country_subgraph(country: str):
    G = build_graph_from_db()
    cnode = f"country:{country}"
    if cnode not in G:
        return None
    SG = nx.Graph()
    SG.add_node(cnode, **G.nodes[cnode])
    for neighbor in G.neighbors(cnode):
        SG.add_node(neighbor, **G.nodes[neighbor])
        SG.add_edge(cnode, neighbor, relation=G.edges[cnode, neighbor]["relation"])
    return SG

# ------------------ VISUALIZE ------------------
def visualize_graph_pyviz(G):
    if not G or G.number_of_nodes() == 0:
        return None
    hv_graph = hv.Graph.from_networkx(G, nx.spring_layout)
    return hv_graph.opts(
        opts.Graph(
            node_color='lightblue',
            edge_color='gray',
            width=800,
            height=800,
            node_size=15,
            tools=['hover', 'tap', 'box_select'],
            inspection_policy='nodes'
        )
    )

def get_country_subgraph_wrapper(country: str):
    return build_country_subgraph(country)
