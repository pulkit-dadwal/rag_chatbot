from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["shop"]
collection = db["products"]


collection.insert_many(documents)
collection.find_one({"name": "Laptop"})
collection.find({"price": {"$gt": 500}})