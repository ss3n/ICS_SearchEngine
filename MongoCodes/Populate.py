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

        insertDocument(db, entry)

        ctr+=1
        print ctr 



