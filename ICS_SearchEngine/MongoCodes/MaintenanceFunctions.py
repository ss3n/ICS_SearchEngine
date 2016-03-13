from MongoWrite import *
from MongoInput import *
from VitalConstants import *

'''
Reads each record from MongoDB and edits the anchor list to make it point to links in and out of a page
'''

client=createConnection()
db = selectDatabase(client)
coll = db[FWDIDXCOLL]

def incoming_and_outgoing(coll):
    pass


def driver():
    print FWDIDXCOLL

driver()
