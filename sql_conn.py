import sqlite3

db_path = "db\medicines.db"

def connection():
    return sqlite3.connect(db_path)
     

def execute(query, params=(),fetch="all"):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    if fetch == "one":
        result = cursor.fetchone()
    elif fetch == "none":
        result = None
    else:
        result = cursor.fetchall()

    conn.commit()
    conn.close()

    return result


