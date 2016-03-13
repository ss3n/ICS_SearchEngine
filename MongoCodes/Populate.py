'''
Reads info from a huge set of data and inserts the forward indices
Forward Index Format:
{
    "url" : <url>
    "content" : <content> 
}

    <content>
    {
        "body" : <body>
        "head" : <head>
        "anchors" : <anchors>
        "anchortext" : <anchortext>
    }

    <body> and <head>
    {
        "word" : { "count": <count>
                    "positions" : [<positions>] } 
    }

    <anchortext>
    {
        "incoming" : (url, textcontent)
        "outgoing" : <outgoingurl>
    }
    
'''

import re
from MongoInput import *
from MongoWrite import *
import json
from urlparse import urlparse
from MaintenanceFunctions import *

j = json_provider()
print 'Loading complete... '

client = createConnection()
db = selectDatabase(client, DBNAME)

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

    url = standardize_url(entry.keys()[0])

    if not cleanUrl(url):
        continue
    if url not in dataStore:
        dataStore[url] = entry.values()[0]  # ??
    ctr+=1
    if ctr%1000==0:
        print ctr 

'''
Functions to obtain data of a link and its parent from the data store. 
Currently the datastore is a dictionary.
To use a live database instead of a dictionary, modify the functions below
'''
def linkPresent(link):
    return link in dataStore
def retrieveContent(link):
    return dataStore[link]
def updateContent(link, dat):
    dataStore[link] = dat

#Iteration 2 - Look at each URL, see its anchor tags, resolve paths if any and update anchor info of each
for parent, content in dataStore.iteritems():
    anc = content['anchors']    # anc stores dictionary => urls: {word: {count, position}}
    for i in anc.keys():
        if i.startswith('http'):
            link = standardize_url(i)
        elif i.startswith('mailto') or i=='':
            continue
        else:
            link = expandAnchorLink(i, parent)

        #If link is same as parent, don't add as an incoming or outgoing link
        if link == parent:
            continue


        #Iff link is part of the crawled set of URLs, set incoming and outgoing to parent and link appropriately
        if linkPresent(link):
            dat = retrieveContent(link)
            if 'anchortext' not in dat:
                dat['anchortext']={'incoming':[], 'outgoing':[]}
            dat['anchortext']['incoming'].append((parent, anc[i]))
            updateContent(link, dat)

            dat = retrieveContent(parent)
            if 'anchortext' not in dat:
                dat['anchortext'] = {'incoming':[], 'outgoing':[]}
            dat['anchortext']['outgoing'].append(link)
            updateContent(parent, dat)
    
#Iteration 3 - Insert each URL, content pair into the databse
for url, content in dataStore.iteritems():
    newdic={}
    newdic["url"] = url
    newdic["content"] = content
    insertDocument(db, newdic, FWDIDXCOLL)

print ctr, 'records inserted into database'
