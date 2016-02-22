from pymongo import MongoClient
from datetime import datetime

def createConnection():
    client = MongoClient()
    return client

def selectdb(client):
    db = client.test
    return db

def insertDocument(database, record):
    if database=="HEAD":
        result = db.head.insert_one(record)
    else if database == "BODY":
        result = db.body.insert_one(record)
    else if database == "anchors":
        result = db.body.insert_one(record)
    return result


