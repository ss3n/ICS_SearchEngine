from query import *
import sys
sys.path.insert(0, '../MongoCodes')
from MaintenanceFunctions import standardize_url

querylist = ['mondego', 'machine learning', 'software engineering', 'security', 'student affairs', 'graduate courses', 'Crista Lopes']
querylist.extend(['REST', 'computer games', 'information retrieval'])

f = open('jugaad.txt', 'r')
text = f.read().split('\n')

ctr=0
holmes = Sherlock()
for query in querylist[:10]:
	query = query.lower()
	googresults = text[ctr:ctr+5]
	googresults = [standardize_url(i) for i in googresults]
	ctr+=5

	results = holmes.search(query)
	# print query
	# print results
	# print
	# print googresults
	print query, " : ", NDCG(googresults, results)
