import pandas as pd
import ast
from pathlib import Path
from sql_conn import connection, execute
conn = connection()
cursor = conn.cursor()

CSV_Path= Path(r"data\csv_cleaned.csv")

if not CSV_Path.exists():
    raise FileNotFoundError("CSV File not found")

df = pd.read_csv(CSV_Path)

try:
    with conn:
        for _, row in df.iterrows():
            brand_name = row["brand_name"]
            generic_name1 = row["generic_name1"]
            manufacturer = row["manufacturer"]

            cursor.execute("""
                INSERT OR IGNORE INTO medicines (brand_name, manufacturer, generic_name1)
                VALUES (?, ?, ?)
                """,
                (brand_name, manufacturer, generic_name1)
            )

            cursor.execute("""
                SELECT id FROM medicines
                WHERE brand_name=? AND manufacturer=?
                """, (brand_name, manufacturer))

            medicine_id = cursor.fetchone()[0]

            raw = row["ingredients1"]

            if pd.isna(raw):
                continue
            try:
                ingredients = ast.literal_eval(raw)
            except (ValueError, SyntaxError):
                continue

            for item in ingredients:
                cursor.execute("""
                INSERT INTO ingredients (medicine_id, ingredient_name, strength)
                VALUES (?, ?, ?)    
                """,
                (medicine_id, item["ingredient"], item["strength"])
                )

    conn.commit()
    conn.close()

except Exception as e:
    print("Data load failed", e)