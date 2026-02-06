from ..tools.database import init_db, save_country_data, get_from_graph

init_db()

save_country_data("India", {
    "Capital": "New Delhi",
    "Currency": "Rupee"
})

print(get_from_graph("India", "Capital"))

