from utils import *
from cStringIO import StringIO
from collections import Counter
from operator import itemgetter
import cPickle as pickle

####################
# File segmentator #
####################

class segmentator:
    """ Class for reading the html dictionary database and parsing it into pages """

    def __init__(self, fileName = '../Data/out.pkl'):

        self.html_dict = pickle.load(open(fileName, 'r'))
        self.urls = self.html_dict.keys()
        self.num_pages = len(self.html_dict)
        self.current_urlIX = 0


    def getNextPage(self):

        if self.current_urlIX == self.num_pages:
            return []

        url = self.urls[self.current_urlIX]
        self.current_urlIX += 1

        data = self.html_dict[url]['body']
        return [url, data]

########################
# Token list generator #
########################

def get_tokenLists():
    ''' function reads through out.txt, and returns a list of urls and a list of tokenlists
        each tokenlist is a list of tokens in a crawled page of the corresponding url
    '''

    seg_iter = segmentator()
    t = tokenizer()

    url_list = []
    token_list = []

    while True:

        data = seg_iter.getNextPage()
        if len(data) == 0:
            break

        url_list += [data[0]]

        stream = StringIO(data[1])
        tokens = t.tokenizeFile(stream)
        token_list += [tokens]

    return [url_list, token_list]


#####################
# Stop word remover #
#####################

def remove_stops(tokenList):
    ''' Given a list of tokens, removes all tokens that are English stop words and returns pruned list
        To remove stop words from all the pages, send sum(token_list, []) as input : 
            this will return a single list containing all non-stop words crawled
    '''

    stop_file = open('stop_words.txt', 'r')
    stop_list = stop_file.read().split('\n')
    stop_file.close()

    tokenList = [t for t in tokenList if t not in stop_list]

    return tokenList


##########################
# Counter for subdomains #
##########################

def get_subCount(url_list):
    ''' Given a list of urls, all of which are subdomains of ics.uci.edu, returns a Counter
        containing all subdomains in alphabetical order along with the number of times they occur in url_list
    '''

    n = len(url_list)
    sub_list = []

    for i in xrange(n):
        sub_list += [ url_list[i].split('ics.uci.edu')[0] ]
        sub_list[i] = sub_list[i].split('/')[-1]
        sub_list[i] = sub_list[i].split('.')[-2]

    count = Counter(sub_list)
    del count['www']
    
    return sorted(count.items(), key=itemgetter(0))