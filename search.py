from sql_conn import execute

def medicine_row_format(row):
    return{
        "id": row[0],
        "brand_name": row[1],
        "manufacturer": row[2],
        "ingredient_name1": row[3],
        "strength1": row[4],
        "ingredient_name2": row[5],
        "strength2": row[6]
    }

BASE_MED_SELECT ="""
SELECT m.id, m.brand_name, m.manufacturer, i.ingredient_name1, i.strength2, i.ingredient_name2, i.strength2
FROM medicines m
JOIN ingredients i ON m.id = i.medicine_id
"""

def unified_search(term):

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
    print(ranked)
    grouped_results = []
    seen = {}

    for med in ranked:
        med_id = med["id"]

        if med_id not in seen:
            seen[med_id] = {
            "id": med_id,
            "brand_name": med["brand_name"],
            "manufacturer": med["manufacturer"],
            "ingredients": [],
            "reason": med["reason"] 
            }

        seen[med_id]["ingredients"].append({
            "name": med["ingredient_name"],
            "strength": med["strength"]
        })
    
    grouped_results = list(seen.values())
    return grouped_results

def run_search(where, params):
    query= BASE_MED_SELECT + " " + where
    rows = execute(query, params)
    return [medicine_row_format(row) for row in rows]

def search_by_name(term):
    return run_search("""WHERE LOWER(m.brand_name) LIKE LOWER(?)""", (f"%{term}%",))

def search_by_ingredient(term):
    return run_search("""WHERE LOWER(i.ingredient_name1) LIKE LOWER(?)""", (f"%{term}%",))
    
if __name__ == "__main__":
    results = unified_search("allegra")
    print(results)        
        #print(row["brand_name"], "-", row["reason"])