from sql_conn import conn, execute

execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand_name TEXT NOT NULL,
        manufacturer TEXT,
        generic_name1 TEXT
    );
""")

execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        ingredient_name TEXT,
        strength TEXT,
        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
    );
""")

execute('''
    CREATE INDEX IF NOT EXISTS idx_medicines_brand
        ON medicines (brand_name);
    CREATE INDEX IF NOT EXISTS idx_medicines_generic
        ON medicines (generic_name1);
    CREATE INDEX IF NOT EXISTS idx_ingredients_name
        ON ingredients (ingredient_name);
''')

conn.commit()
conn.close()
