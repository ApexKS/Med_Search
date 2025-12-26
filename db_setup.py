import sqlite3

conn= sqlite3.connect("medicines.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand_name TEXT NOT NULL,
        manufacturer TEXT,
        generic_name1 TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        ingredient_name TEXT,
        strength TEXT,
        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
    );
""")

conn.commit()
conn.close()
