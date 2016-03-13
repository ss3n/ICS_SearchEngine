#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Derived from the code of original author: Rohan Achar ra.rohan@gmail.com
'''
import re
import cPickle as pickle

try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs

from Crawler4py.Config import Config

def num_query_args_less_than_2(string):
    if string.count('&') > 1:
        return False
    else:
        return True

def check_if_no_loop(string):
    x=string.split('/')
    for i in x:
        t=x.count(i)
        if t>5:
            return False
    return True

def url_length_lessthan_512(string):
    return len(string) <= 512

def num_slashes_lessthan_10(string):
    return string.count('/') <= 10

def is_not_query(string):
    if len(string) == 0:
        return True
    else:
        return False

def is_not_eppstein(string):
    if 'eppstein' in string:
        return False
    else:
        return True

def is_not_blacklisted(string):
    blacklist = ['gonet', 'sli', 'evoke', 'fano', 'mlearn']
    
    for bl in blacklist:
        if bl in string:
            return False
    
    return True

class MyConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.UserAgentString = "IR W16 WebCrawler 75307532_92707006_48565650"
        self.MaxWorkerThreads = 12
    self.PolitenessDelay = 500
    self.UrlFetchTimeOut = 300
    self.OutBufferTimeOut = 3600
    self.DepthFirstTraversal = True
    self.MaxDepth = 5

    def GetSeeds(self):
        '''Returns the first set of urls to start crawling from'''
        return ["http://www.ics.uci.edu/"]

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''
        print(parsedData["url"])

        self.fptr = open("out.pkl", 'a')
        p_obj = pickle.dumps(parsedData,2)
        self.fptr.write(p_obj)
        self.fptr.write('....swarun...,,,,,arjun,,,....shiladitya....')

        #self.fptr.write(parsedData["url"]+'\n')
        #self.fptr.write(parsedData["text"].encode("U7"))
        #self.fptr.write("\n....swarun...,,,,,arjun,,,....shiladitya....\n")
        
        self.fptr.close()
        #print(parsedData["text"])
        return

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        parsed = urlparse(url)
        try:
            return ".ics.uci.edu" in parsed.hostname \
        and num_query_args_less_than_2(parsed.query) \
        and check_if_no_loop(parsed.path.lower()) \
        and url_length_lessthan_512(parsed.hostname +'/'+ parsed.path) \
        and num_slashes_lessthan_10(parsed.path) \
        and is_not_blacklisted(parsed.hostname) \
                and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                + "|thmx|mso|arff|rtf|jar|csv"\
                + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) 

        except TypeError:
            print ("TypeError for ", parsed)


