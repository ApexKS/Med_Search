from sql_conn import connection, execute

def medicine_row_format(row):
    return{
        "id": row[0],
        "brand_name": row[1],
        "manufacturer": row[2],
        "ingredient_name": row[3],
        "strength": row[4]
    }

BASE_MED_SELECT ="""
SELECT m.id, m.brand_name, m.generic_name1, m.manufacturer, i.ingredient_name, i.strength
FROM medicines m
JOIN ingredients i ON m.id = i.medicine_id
"""

def run_search(where, params):
    query= BASE_MED_SELECT + " " + where
    rows = execute(query, params)
    return [medicine_row_format(row) for row in rows]

def search_by_name(term):
    return run_search("""WHERE LOWER(m.brand_name) LIKE LOWER(?)""", (f"%{term}%",))

def search_by_ingredient(term):
    return run_search("""
            WHERE LOWER(i.ingredient_name) LIKE LOWER(?)""",(f"%{term}%",))
    
if __name__ == "__main__":
    results = search_by_name("cef")
    for row in results:
        print(row)