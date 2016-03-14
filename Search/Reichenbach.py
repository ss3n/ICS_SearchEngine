#Final Battle : Sherlock or Moriarty?!

#DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! 
import sys
from query import *
sys.path.insert(0, '../MongoCodes')
from MaintenanceFunctions import standardize_url
import urllib

'''
- Calls Sherlock with the querystring and obtains results from Sherlock
- Calls Moriarty with the googleresults
- Compares Results and returns NDCG

'''

def commenceBattle(querystring, googleresults):
	holmes = Sherlock(3)
	sherlockResult = holmes.search(querystring)
	print sherlockResult
	print googleresults

	print NDCG(sherlockResult, googleresults)

def getGoogleResults(googleResultsString):
	spl = googleResultsString.split(GOOGLE_RESULTS_DELIM)
	spl = [standardize_url(urllib.unquote(i)) for i in spl]
	return spl

def main():
	querystring = (sys.argv[1]).lower()
	querystring = urllib.unquote(querystring)
	googleresults = getGoogleResults(sys.argv[2])

	print querystring
	print

	commenceBattle(querystring, googleresults)

main()