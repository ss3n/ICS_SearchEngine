from SearchConstants import *
from pymongo import MongoClient
from MongoWrite import *
import operator

class Sherlock:
    '''
        Class for handling queries and performing search: outputs list of <k> most relevant urls
    '''

    def __init__(self, search_size = 10):
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


    def search(self, query):
        '''
            Returns a list of 2-tuples: (<url>, <relevance_score>)
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
        ranking = [rank[0].encode('ascii') for rank in ranking[:self.search_size]]
        return ranking



class Moriarty:
    '''
        Class that takes in a query and returns top <k> search results from Google search
    '''
    def __init__(self, search_size = 10):
        self.search_size = search_size

    def search(self, query):
        '''function takes in a string query and returns a list of <k> Google search results
            sorted by descending order of relevance
        '''