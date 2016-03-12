'''
Has a set of library functions that can be used for:
    - Creating a connection to a local (or network) Mongo DB
    - Selecting a database
    - Inserting record(s) into a collection
'''
from pymongo import MongoClient
from datetime import datetime
from VitalConstants import *

#Create Connection : returns client with connection to local MongoClient
def createConnection(host='localhost', port=27017):
    client = MongoClient(host, port)
    return client

#Select DB : Returns MongoDB DB object   
def selectDatabase(client, dbname=DBNAME):
    db = client[dbname]
    return db

#db - database object
#collection - string representing collection
#record - Record containging JSON-like data
def insertDocument(db, record=None, collection='ir'):
    result = db[collection].insert(record, check_keys=False)
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
