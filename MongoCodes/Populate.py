'''
Reads info from a huge set of data and inserts the forward indices
'''
from MongoInput import *
from MongoWrite import *
import json
from urlparse import urlparse

j = json_provider()
print 'Loading complete... '

client = createConnection()
db = selectDatabase(client, DBNAME)

def standardize_url(url):
    return url.lstrip('http').lstrip('s').lstrip('://').lstrip('www.')

def expandAnchorLink(url, parent):
    if 'href' in url:
        print url
        return None
    else:
        return None

    if 'http' == url[:4]:
        return url
    elif url == '':
        return parent
    elif url[:3] == '../':
        o = urlparse(parent)
        print o.path, url
        return url

def cleanUrl(url):
    if 'href' not in url:
        return True
    return False
    


ctr=0
anchorset = {}
'''First iteration store each url:content in memory
Second iteration look at anchor tags, resolve any paths and update anchor info
Third Iteration insert everything into database
'''

#Iteration 1 - Adding each valid URL into a content list
dataStore = {}
while True:
    entry = j.getNext()
    if len(entry) == 0:
        break

    newdic = {}
    print entry.keys()[0]
    url = standardize_url(entry.keys()[0])
    if url not in dataStore:
        dataStore[url] = entry.values()[0]
    else:
        print url

    ctr+=1
    if ctr%1000==0:
        print ctr 

#Iteration 2 - Look at each URL, see its anchor tags, resolve paths if any and update anchor info of each
if False:
    anc  = newdic['content']['anchors']
    for url in anc.keys():
        if cleanUrl(url):
            expandAnchorLink(url, newdic['url'])
#Iteration 3 - Insert each URL, content pair into the databse
if False:
    newdic["url"] = standardize_url(entry.keys()[0])
    newdic["content"] = entry.values()[0]
#        insertDocument(db, newdic, FWDIDXCOLL)

print ctr, 'records inserted into database'



