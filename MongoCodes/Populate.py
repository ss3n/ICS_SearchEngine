from MongoInput import *
from MongoWrite import *
import json

j = json_provider()
print 'Loading complete... '

client = createConnection()
db = selectdb(client, 'irindexer')

ctr=0
while True:
	entry = j.getNext()
	if len(entry) == 0:
		break

        newdic = {}
        newdic["url"] = entry.keys()[0]
        newdic["content"] = entry.values()[0]

        insertDocument(db, newdic)

        ctr+=1
        if ctr%100==0:
            print ctr 



