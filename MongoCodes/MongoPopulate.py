from MongoInput import *
from MongoWrite import *
import json

j = json_provider()

ctr = 1
client = createConnection()
db = selectDatabase(client)
while True:

	entry = j.getNext()

	if len(entry) == 0:
		break

	print ctr
	ctr+=1

	result = insertDocument(db, entry)