# verify_graph.py
from ..tools.database import get_country_subgraph, visualize_graph_pyviz
from holoviews import save

G = get_country_subgraph('India')
hv_graph = visualize_graph_pyviz(G)
if hv_graph:
    save(hv_graph, "india_graph.html")  # Opens interactive HTML
    print("✅ Graph saved successfully!")
else:
    print("❌ No graph to visualize.")

