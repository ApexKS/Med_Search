import pandas as pd
import re

df = pd.read_csv(r"csvs\indian_medicine_data.csv")        #importing the csv file

#displaying data
#print(df.head())                                    
#print(df.columns)
#print(df.info())

#renaming columns
df = df.rename(columns={
    "name": "brand_name",
    "short_composition1": "comp1",
    "short_composition2": "comp2",
    "manufacturer_name": "manufacturer"
})

#removing extra space and maintaining case
df["brand_name"] = df["brand_name"].str.strip().str.title()
df["manufacturer"] = df["manufacturer"].str.strip().str.title()

#remove empty rows
df = df.dropna(subset=["brand_name","comp1"])

#remove duplicates
df = df.drop_duplicates(subset=["brand_name", "comp1", "comp2"])

#parsing(correcting) entries in csv
def parse(composition):
    if not isinstance(composition, str):
        return []
    
    composition = composition.strip()

    match = re.match(r"(.*?)\s*\((.*?)\)", composition)            #separating name (amount)

    if match:
        name = match.group(1).strip()
        strength = match.group(2).strip()

    else:
        name = composition
        strength = None

    return [{
        "ingredient": name,
        "strength": strength
    }]  
    
df["ingredients1"] = df["comp1"].apply(parse)
df["ingredients2"] = df["comp2"].apply(parse)
df["generic_name1"] = df["ingredients1"].apply(lambda x: x[0]["ingredient"] if x else None)
df["generic_name2"] = df["ingredients2"].apply(lambda x: x[0]["ingredient"] if x else None)

#print(df[["brand_name","comp","generic name"]].head(10))

final_columns = ["brand_name", "generic_name1", "generic_name2", "ingredients1", "ingredients2", "manufacturer"]

df_final = df[final_columns]

df_final.to_csv(r"csvs\indian_medicine_data.csv", index=False)