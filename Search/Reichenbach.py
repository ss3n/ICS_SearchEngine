#Final Battle : Sherlock or Moriarty?!

#DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! DID YOU MISS ME! 
import sys
from query import *
sys.path.insert(0, '../MongoCodes')
from MaintenanceFunctions import standardize_url
import urllib
import urllib2
from bs4 import BeautifulSoup

'''
- Calls Sherlock with the querystring and obtains results from Sherlock
- Calls Moriarty with the googleresults
- Compares Results and returns NDCG
'''


def getResultsJson(sherlockResult):
	def getTitle(url):
		url = 'http://'+url
		soup = BeautifulSoup(urllib2.urlopen(url))
		return soup.title.string

	resultsJson = {'items':[]}
	for url in sherlockResult:
		item = {}
		item['itemheading'] = getTitle(url)
		item['itemURL'] = url
		item['itemcontent'] = ''
		resultsJson['items'].append(item)
	return resultsJson




def commenceBattle(querystring, googleresults):
	print 'Searching for : ', querystring
	print 
	holmes = Sherlock()
	sherlockResult = holmes.search(querystring)

	print NDCG(googleresults, sherlockResult)

	return getResultsJson(sherlockResult)

def getGoogleResults(googleResultsString):
	spl = googleResultsString.split(GOOGLE_RESULTS_DELIM)
	spl = [standardize_url(urllib.unquote(i)) for i in spl]
	return spl

def main():
	querystring = (sys.argv[1]).lower()
	querystring = urllib.unquote(querystring)
	querystring = querystring.replace('+',' ')
	googleresults = getGoogleResults(sys.argv[2])

	results = commenceBattle(querystring, googleresults)
	print results

main()