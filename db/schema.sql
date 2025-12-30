CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand_name TEXT NOT NULL,
        manufacturer TEXT,
        generic_name1 TEXT,
        generic_name2 TEXT,
        UNIQUE (brand_name, manufacturer)
);

CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicine_id INTEGER,
        ingredient_name1 TEXT,
        strength1 TEXT,
        ingredient_name2 TEXT,
        strength2 TEXT,
        FOREIGN KEY (medicine_id) REFERENCES medicines(id)
    );

CREATE INDEX IF NOT EXISTS idx_medicines_brand
        ON medicines (brand_name);
CREATE INDEX IF NOT EXISTS idx_medicines_generic1
        ON medicines (generic_name1);
CREATE INDEX IF NOT EXISTS idx_medicines_generic2
        ON medicines (generic_name2);
CREATE INDEX IF NOT EXISTS idx_ingredients_name1
        ON ingredients (ingredient_name1);
CREATE INDEX IF NOT EXISTS idx_ingredients_name2
        ON ingredients (ingredient_name2);