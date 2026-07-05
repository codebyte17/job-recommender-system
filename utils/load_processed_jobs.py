import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("../datasets/processed/integrated_dataset.v2.csv")

client = MongoClient('mongodb://localhost:27017/')
db = client['jobs-db']
collection = db['jobs']
records = df.to_dict(orient="records")

result = collection.insert_many(records)

print(f"Inserted {len(result.inserted_ids)} documents.")


