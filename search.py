import sqlite3

def get_connection():
    return sqlite3.connect("medicines.db")

def get_ingredients(medicine_id, cursor):
    cursor.execute('''
                    SELECT ingredient_name, strength
                    FROM ingredients
                    WHERE medicine_id = ?
                    ''',
                    (medicine_id,)
                    )
    return cursor.fetchall()


def search_by_name(term):
    conn= get_connection()
    cursor = conn.cursor()

    query = '''SELECT id, brand_name, generic_name1, manufacturer
                FROM medicines
                WHERE LOWER(brand_name) LIKE LOWER(?)'''

    cursor.execute(query, (f"%{term}%",))

    medicines = []

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
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
            SELECT m.id, m.brand_name, m.generic_name1, m.manufacturer
            FROM medicines m
            JOIN ingredients i ON m.id = i.medicine_id
            WHERE LOWER(i.ingredient_name) LIKE LOWER(?)'''
    
    cursor.execute(query, (f"%{term}%",))
#    return cursor.fetchall()

    medicines = []

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
    results = search_by_ingredient("cef")
    for row in results:
        print(row)