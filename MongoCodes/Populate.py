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

        print type(entry)
	#rec = json.dumps(entry)
        insertDocument(db, entry)
        #print type(rec)
        #insertDocument(db, rec)

        ctr+=1
        print ctr 



