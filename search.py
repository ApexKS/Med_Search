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
SELECT m.id, m.brand_name, m.manufacturer, i.ingredient_name, i.strength
FROM medicines m
JOIN ingredients i ON m.id = i.medicine_id
"""

def unified_search(term):
    conn = connection()
    cursor = conn.cursor()

    term_l = term.lower()
    results = {}

    for row in search_by_name(term):
        id = row["id"]
        brand = row["brand_name"]
        manu = row["manufacturer"]
        ing = row["ingredient_name"]
        strength = row["strength"]

        score = 0
        brand_l = brand.lower()

        if term_l == brand_l:
            score += 100
        elif brand_l.startswith(term_l):
            score += 70
        elif term_l in brand_l:
            score += 40
        
        results[id]= {
            "id": id,
            "brand_name": brand,
            "manufacturer": manu,
            "ingredient_name": ing,
            "strength": strength,
            "score": score,
            "reason": "brand"
        }

    for row in search_by_ingredient(term):
        id = row["id"]
        brand = row["brand_name"]
        manu = row["manufacturer"]
        ing = row["ingredient_name"]
        strength = row["strength"]

        score = 0
        ing_l = ing.lower()

        if ing_l == term_l:
            score += 60
        elif term_l in ing_l:
            score += 30

        if id in results:
            results[id]["score"] += score
            results[id]["reason"] += "+ingredient"
        else:  
            results[id]= {
            "id": id,
            "brand_name": brand,
            "manufacturer": manu,
            "ingredient_name": ing,
            "strength": strength,
            "score": score,
            "reason": "ingredient"
        }
    
    ranked = sorted(results.values(), key=lambda x: x["score"], reverse=True)

    for i in ranked:
        i.pop("score")
    
    return ranked

def run_search(where, params):
    query= BASE_MED_SELECT + " " + where
    rows = execute(query, params)
    return [medicine_row_format(row) for row in rows]

def search_by_name(term):
    return run_search("""WHERE LOWER(m.brand_name) LIKE LOWER(?)""", (f"%{term}%",))

def search_by_ingredient(term):
    return run_search("""WHERE LOWER(i.ingredient_name) LIKE LOWER(?)""",(f"%{term}%",))
    
if __name__ == "__main__":
    results = unified_search("paracetamol")
    for row in results:
        print(row["brand_name"], "-", row["reason"])