# app.py
import streamlit as st
import streamlit.components.v1 as components
import re
import networkx as nx

from tools.database import (
    get_country_data,
    save_country_data,
    get_country_subgraph_wrapper,
    get_from_graph
)
from tools.scraper import fetch_country_infobox
import holoviews as hv
from bokeh.embed import file_html
from bokeh.resources import CDN

st.set_page_config(page_title="Country Info Agent", layout="wide")
st.title("🌐 Country Information Agent")

# ----------------- USER INPUT -----------------
user_query = st.text_input("Ask about a country:", "")

if user_query:
    # ----------------- PARSE QUERY -----------------
    country_match = re.search(r'of\s+([a-zA-Z\s]+)', user_query.lower())
    if country_match:
        country_name = country_match.group(1).title().strip()
    else:
        # fallback: last word is country
        country_name = user_query.title().strip()

    # Attempt to extract attribute(s) from query
    attribute_patterns = ["capital", "population", "currency", "leader", "president", "pm",
                          "official languages", "religion", "density", "gdp", "hdi", "calling code"]
    attributes_requested = []
    for attr in attribute_patterns:
        if attr in user_query.lower():
            attributes_requested.append(attr)

    if not attributes_requested:
        st.error("❌ Could not identify attribute in your query.")
    else:
        # ----------------- GET COUNTRY DATA -----------------
        data = get_country_data(country_name)
        if not data:
            st.info(f"🔎 Fetching data for **{country_name}**...")
            try:
                data = fetch_country_infobox(country_name)
                if data:
                    save_country_data(country_name, data)
                    st.success(f"✅ Data for **{country_name}** fetched and saved!")
                else:
                    st.error(f"❌ Could not fetch data for '{country_name}'")
                    data = None
            except Exception as e:
                st.error(f"❌ Could not fetch data for '{country_name}': {e}")
                data = None

        if data:
            # ----------------- DISPLAY ONLY REQUESTED ATTRIBUTES -----------------
            for attr in attributes_requested:
                # First try graph
                val = get_from_graph(country_name, attr)
                if not val:
                    # fallback to DB dictionary
                    for key, value in data.items():
                        if attr.replace(" ", "").lower() in key.replace("_", "").lower():
                            val = value
                            break

                if val:
                    st.info(f"**{attr.title()} of {country_name}:** {val}")
                else:
                    st.warning(f"⚠️ {attr.title()} data not available for {country_name}.")

            # ----------------- SHOW GRAPH -----------------
            if st.button("Show Graph"):
                G_nx = get_country_subgraph_wrapper(country_name)
                if G_nx and G_nx.number_of_nodes() > 0:
                    hv_graph = hv.Graph.from_networkx(G_nx, nx.spring_layout)
                    hv_graph = hv_graph.opts(
                        hv.opts.Graph(
                            node_color='lightblue',
                            edge_color='gray',
                            width=800,
                            height=800,
                            node_size=15,
                            tools=['hover', 'tap', 'box_select'],
                            inspection_policy='nodes'
                        )
                    )
                    html = file_html(hv_graph, CDN, f"{country_name} Graph")
                    components.html(html, height=800, scrolling=True)
                else:
                    st.warning("⚠️ No graph data available for this country.")
