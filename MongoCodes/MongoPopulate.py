from MongoInput import *
from MongoWrite import *
import json

j = json_provider()

while True:

	entry = j.getNext()

	if len(entry) == 0:
		break

	jsonout = json.dumps(entry)
	print jsonout