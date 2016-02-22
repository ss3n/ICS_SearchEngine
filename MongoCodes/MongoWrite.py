from pymongo import MongoClient
from datetime import datetime
client = MongoClient()

db = client.test
result = db.restaurant.insert_one()
print result.inserted_id

