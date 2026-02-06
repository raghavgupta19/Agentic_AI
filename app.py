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
    attribute_patterns = {
        "pm": ["pm", "prime_minister", "prime minister", "premier"],
        "president": ["president"],
        "capital": ["capital"],
        "population": ["population"],
        "currency": ["currency"],
        "official languages": ["official languages", "language"],
        "religion": ["religion"],
        "density": ["density"],
        "gdp": ["gdp"],
        "hdi": ["hdi"],
        "calling code": ["calling code", "code"]
    }
    attributes_requested = []
    query_lower = user_query.lower()
    for standard_attr, patterns in attribute_patterns.items():
        for pattern in patterns:
            if pattern in query_lower:
                attributes_requested.append(standard_attr)
                break

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
                val = None
                
                # First try graph with fuzzy matching
                val = get_from_graph(country_name, attr)
                
                # Fallback to DB dictionary with better matching
                if not val:
                    attr_normalized = attr.lower().replace(" ", "").replace("_", "")
                    for key, value in data.items():
                        key_normalized = key.lower().replace(" ", "").replace("_", "")
                        # Check if either contains the other
                        if attr_normalized in key_normalized or key_normalized in attr_normalized:
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
                    try:
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
                        # Convert to bokeh plot before embedding
                        bokeh_plot = hv.render(hv_graph)
                        if bokeh_plot:
                            html = file_html(bokeh_plot, CDN, f"{country_name} Graph")
                            components.html(html, height=800, scrolling=True)
                        else:
                            st.warning("⚠️ Could not render graph visualization.")
                    except Exception as e:
                        st.error(f"❌ Error rendering graph: {e}")
                else:
                    st.warning("⚠️ No graph data available for this country.")
