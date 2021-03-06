from SearchConstants import *
from pymongo import MongoClient
from MongoWrite import *
import operator
from numpy import log2 as log
from VitalConstants import *
'''
TODO
- Integrate Moriarty with Arjun's php server
- Integrate PageRank into Sherlock?
'''
###############################
# class for our search engine #
###############################

class Sherlock:
    '''
        Class for handling queries and performing search: outputs list of <k> most relevant urls
    '''

    def __init__(self, search_size = 5):
        self.client=createConnection()
        self.db = selectDatabase(self.client)
        self.search_size = search_size

    def retrieve(self, terms, INVCOLL):
        coll = self.db[INVCOLL]
        retrieve_dict = {}
        all_urls = []

        for term in terms:
            retrieve_dict[term] = {}

            for entry in coll.find({"term":term}, {"content":1}):
                content = entry['content']

                for url in content.keys():
                    content_dict = {}
                    content_dict['value'] = content[url]['value']
                    content_dict['positions'] = content[url]['positions']

                    retrieve_dict[term][url] = content_dict
                    all_urls += [url]

        all_urls = list(set(all_urls))

        relevance_dict = {}
        for url in all_urls:
            value = 0
            for term in terms:
                if url in retrieve_dict[term]:
                    value += retrieve_dict[term][url]['value']
            relevance_dict[url] = value

        return relevance_dict


    def searchQuery(self, query):
        '''
            Returns a list of 2-tuples (<url>, <score>) ranked by relevance
        '''
        terms = query.split()

        head_search = self.retrieve(terms, INVHEADCOLL)
        body_search = self.retrieve(terms, INVBODYCOLL)
        anchor_search = self.retrieve(terms, INVANCHORCOLL)

        all_urls = list(set(head_search.keys() + body_search.keys() + anchor_search.keys()))

        relevance_dict = {}
        for url in all_urls:
            value = 0
            if url in head_search:
                value += HEAD_WT*head_search[url]
            if url in body_search:
                value += BODY_WT*body_search[url]
            if url in anchor_search:
                value += ANCHOR_WT*anchor_search[url]
            relevance_dict[url] = value

        ranking = sorted(relevance_dict.items(), key=operator.itemgetter(1), reverse=True)
        return ranking


    def search(self, query):
        '''
            Returns top <search_size> search results as a list of urls in ranked order
        '''
        results = self.searchQuery(query)
        results = [result[0].encode('ascii') for result in results]
        return results[:self.search_size]

    def findRelevantSnippet(self, query, snippets):
        def findRelevantSnip(query, snip):
            if len(snip) < 200:
                return 0, len(snip)
            someWordMatched = False
            for word in query.split():
                loc = snip.find(word)
                sniplen = len(snip)
                if loc == -1:
                    continue
                else:
                    start = max(0, loc-50)
                    finish = min(sniplen, loc+150)
                    return start, finish

            if not someWordMatched:
                return 0, 200

        query = query.lower()
        result = []
        for snippet in snippets:
            snip = snippet.lower()
            start, finish = findRelevantSnip(query, snip)
            result.append(snippet[start:finish])

        return result


    def getSnippets(self, query, searchResults):
        def getSnippetForUrl(url):
            body = ''
            for entry in coll.find({"url":url}, {"body":1}):
                body = entry['body']
            return body

        resultSnippets = []
        coll = self.db[SNIPPETS_COLL]

        for url in searchResults:
            snippet = getSnippetForUrl(url)            
            resultSnippets.append(snippet)

        result = self.findRelevantSnippet(query, resultSnippets)

        return result


####################################
# class for Google's search engine #
####################################

class Moriarty:
    '''
        Class that takes in a query and returns top <k> search results from Google search
    '''
    def __init__(self, search_size = 5):
        self.search_size = search_size

    def search(self, query):
        '''function takes in a string query and returns a list of <k> Google search results
            sorted by descending order of relevance
        '''


########################
# Thou shalt be judged #
########################

def sanitizeResults(arr):
    return [i.rstrip('/') for i in arr]

def NDCG(ideal, results):
    '''
        Given a list of ideal and obtained result URLs in descending rank, calculates norm cumulative gain
        NOTE: 1st argument is ideal ranking, 2nd is obtained ranking
    '''
    ideal = sanitizeResults(ideal)
    results = sanitizeResults(results)

    # print ideal
    # print results

    n = len(ideal)
    assert (n == len(results)), 'Ideal results and obtained results must be of same length'+str(n)+' '+str(len(results))

    ideal_relevance = n * [0]
    for i in xrange(n):
        ideal_relevance[i] = n-i

    obtained_relevance = n * [0]
    for i in xrange(n):
        try:
            ideal_ix = ideal.index(results[i])
            obtained_relevance[i] = ideal_relevance[ideal_ix]

        except ValueError:
            pass
    
    idcg = ideal_relevance[0]
    for i in xrange(1,n):
        idcg += ideal_relevance[i]/log(i+1)

    dcg = obtained_relevance[0]
    for i in xrange(1,n):
        dcg += obtained_relevance[i]/log(i+1)
    
    # print idcg, dcg
    return dcg/idcg