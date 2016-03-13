from SearchConstants import *
from pymongo import MongoClient
from MongoWrite import *

class sherlock:
    '''
        Class for handling queries and performing search: outputs list of <k> most relevant urls
    '''

    def __init__(self):
        client=createConnection()
        db = selectDatabase(client)

    def retrieve(self, terms, INVCOLL):
        coll = self.db[INVCOLL]
        retrieve_dict = {}

        for term in terms:
            for entry in coll.find({"term":term}, {"content":1}):
                content = entry['content']

                for url in content.keys():


    def searchQuery(self, query):
        terms = query.split()

        head_search = retrieve(terms, INVHEADCOLL)
        body_search = retrieve(terms, INVBODYCOLL)
        anchor_search = retrieve(terms, INVANCHORCOLL)