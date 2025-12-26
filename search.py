from sql_conn import conn, execute

def get_ingredients(medicine_id, cursor):
    execute('''
                    SELECT ingredient_name, strength
                    FROM ingredients
                    WHERE medicine_id = ?
                    ''',
                    (medicine_id,)
                    )
    return cursor.fetchall()

def medicine_row_format(row):
    return{
        "id": row[0],
        "brand_name": row[1],
        "generic_name": row[2],
        "manufacturer": row[3]
    }

BASE_MED_SELECT ="""
SELECT m.id, m.brand_name, m.generic_name1, m.manufacturer
FROM medicines m
"""

def run_search(where, params):
    query= BASE_MED_SELECT + " " + where
    rows = execute(query, params)
    return [medicine_row_format(row) for row in rows]

def search_by_name(term):
    return run_search('''WHERE LOWER(brand_name) LIKE LOWER(?)''', (f"%{term}%",))

    medicines = []
    cursor = conn.cursor()
    for row in cursor.fetchall():
        med_id, brand, generic, mfg = row
        ingredients = get_ingredients(med_id, cursor)

        medicines.append({
            "brand_name": brand,
            "generic_name1":generic,
            "manufacturer":mfg,
            "ingredients":[
                {"ingredient_name":ing, "strength":strength}
                for ing, strength in ingredients
            ]
        })

    conn.close()
    return medicines

def search_by_ingredient(term):

    query = '''
            SELECT m.id, m.brand_name, m.generic_name1, m.manufacturer
            FROM medicines m
            JOIN ingredients i ON m.id = i.medicine_id
            WHERE LOWER(i.ingredient_name) LIKE LOWER(?)'''
    
    execute(query, (f"%{term}%",))

    medicines = []
    cursor = conn.cursor()
    for row in cursor.fetchall():
        med_id, brand, generic, mfg = row
        ingredients = get_ingredients(med_id, cursor)

        medicines.append({
            "brand_name": brand,
            "generic_name1":generic,
            "manufacturer":mfg,
            "ingredients":[
                {"ingredient_name":ing, "strength":strength}
                for ing, strength in ingredients
            ]
        })

    conn.close()
    return medicines

if __name__ == "__main__":
    results = search_by_name("cef")
    for row in results:
        print(row)