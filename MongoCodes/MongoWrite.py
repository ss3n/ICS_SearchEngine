from pymongo import MongoClient
from datetime import datetime

def createConnection():
    client = MongoClient()
    return client

def selectdb(client, dbname='test'):
    db = client.test
    return db

def insertDocument(db, collection, record):
    if collection=="head":
        result = db.head.insert_one(record)
    else if collection == "body":
        result = db.body.insert_one(record)
    else if collection == "anchors":
        result = db.anchors.insert_one(record)

    return result

def bulkInsert():
    pass

'''
url:
    head:
        words:frequency
    body:
        words:frequency
    anchors:
        words:frequency

(url, dictionary)
dictionary = {head: , body:, anchors: }
'''
