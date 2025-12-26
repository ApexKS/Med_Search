from pathlib import Path
import sqlite3

DB_Path= r"db\medicines.db"
Schema_Path= Path(__file__).parent / "schema.sql"

def init_db():
    conn= sqlite3.connect(DB_Path)
    with open(Schema_Path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.close()

if __name__ == "__main__":
    init_db()
