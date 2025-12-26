import sqlite3
import pandas as pd
import ast
from sql_conn import conn, execute

execute("DELETE FROM ingredients")
execute("DELETE FROM medicines")
conn.commit()

df = pd.read_csv(r"csvs\indian_medicine_data.csv")

for _, row in df.iterrows():
    brand_name = row["brand_name"]
    generic_name1 = row["generic_name1"]
    manufacturer = row["manufacturer"]

    execute("""
        INSERT INTO medicines (brand_name, manufacturer, generic_name1)
        VALUES (?, ?, ?)
    """,
        (brand_name, manufacturer, generic_name1)
    )

    cursor = conn.cursor()
    medicine_id = cursor.lastrowid

    ingredients = ast.literal_eval(row["ingredients1"])

    for item in ingredients:
        execute("""
        INSERT INTO ingredients (medicine_id, ingredient_name, strength)
        VALUES (?, ?, ?)    
    """,
        (medicine_id, item["ingredient"], item["strength"])
        )

conn.commit()
conn.close()