'''
Reads info from a huge set of data and inserts the forward indices
'''
from MongoInput import *
from MongoWrite import *
import json

j = json_provider()
print 'Loading complete... '

FWDIDXCOLL = 'fwdIX100'
DBNAME = 'irindexer'

client = createConnection()
db = selectDatabase(client, DBNAME)

ctr=0
while True:
	entry = j.getNext()
	if len(entry) == 0:
		break

        newdic = {}
        newdic["url"] = entry.keys()[0]
        newdic["content"] = entry.values()[0]

        insertDocument(db, newdic, FWDIDXCOLL)

        ctr+=1
        if ctr%1000==0:
            print ctr 

print ctr, 'records inserted into database'



