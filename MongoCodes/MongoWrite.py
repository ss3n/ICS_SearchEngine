from pymongo import MongoClient
from datetime import datetime

#Create Connection : returns client with connection to local MongoClient
def createConnection(host='localhost', port=27017):
    client = MongoClient(host, port)
    return client

#Select DB : Returns MongoDB DB object   
def selectDatabase(client, dbname='irindexer'):
    db = client[dbname]
    return db

#db - database object
#collection - string representing collection
#record - Record containging JSON-like data
def insertDocument(db, record=None, collection='fwdindex'):
    result = db[collection].insert(record, check_keys = False)
    return result

#Bulk Inserts many records into Database
'''Input format is:
    url:
        head:
            wordlist
        body:
            wordlist
        anchor:
            wordlist
'''
def bulkInsert(db, manyrecords):
    results=[]
    for collection, record in manyrecords:
        results+= db[collection].insert_many(record)
    return results

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
