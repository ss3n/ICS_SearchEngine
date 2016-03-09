'''
Reads info from a huge set of data and inserts the forward indices
'''
import re
from MongoInput import *
from MongoWrite import *
import json
from urlparse import urlparse

j = json_provider()
print 'Loading complete... '

client = createConnection()
db = selectDatabase(client, DBNAME)

'''
Removes HTTP/HTTPS and :// and www. prefixes to avoid URL duplication
'''
def standardize_url(url):
    def removePrefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text
    url = removePrefix(url, 'https')
    url = removePrefix(url, 'http')
    url = removePrefix(url, '://')
    url = removePrefix(url, 'www.')
    return url.rstrip('/')

'''
Expands Local Anchor Links
- If anchor link starts with ? or # append link to parent url
- If anchor link contains ../ go up the path appropriately and append
'''
def expandAnchorLink(url, parent):
    def findSlashes(text):
        loc = [i for i in range(len(text)) if text[i]=='/']
        return loc

    if url[0]=='?':
        if parent[-1]=='/':
            return parent+url
        return parent + '/' + url

    elif url[0] == '#':
        return parent+url

#    elif url[:3] == '../':
    else:
        levelsUp = url.count('../')+1
        while url.startswith('../'):
            url = url[3:]

        levelsUp = min(levelsUp, parent.count('/'))
        loc = findSlashes(parent)

        ans = parent[:loc[len(loc)-levelsUp]+1] + url
        return ans



def cleanUrl(url):
    if 'href' in url:
        return False
    if 'mailto' in url:
        return False
    if re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4|txt|gz|py"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", url) :
        return False
    return True
    


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

    url = standardize_url(entry.keys()[0])

    if not cleanUrl(url):
        continue
    if url not in dataStore:
        dataStore[url] = entry.values()[0]
    ctr+=1
    if ctr%1000==0:
        print ctr 

def linkPresent(link):
    return link in dataStore
def retrieveContent(link):
    return dataStore[link]

print linkPresent('http://store.apple.com')
#Iteration 2 - Look at each URL, see its anchor tags, resolve paths if any and update anchor info of each
for parent, content in dataStore.iteritems():
    anc = content['anchors']
    for i in anc.keys():
        if i.startswith('http'):
            link = standardize_url(i)
        elif i.startswith('mailto') or i=='':
            continue
        else:
            link = expandAnchorLink(i, parent)

        if linkPresent(link):
            dat = retrieveContent(link)
            if 'anchortext' not in dat:
                dat['anchortext']={'incoming':[], 'outgoing':[]}
                dat['anchortext']['incoming'].append((link, anc[i]))
            if 'anchortext' not in dataStore[parent]:
                dat['anchortext']={'incoming':[], 'outgoing':[]}
                dat['anchortext']['outgoing'].append((link, anc[i]))
                


    
#Iteration 3 - Insert each URL, content pair into the databse
if False:
    newdic={}
    newdic["url"] = standardize_url(entry.keys()[0])
    newdic["content"] = entry.values()[0]
#        insertDocument(db, newdic, FWDIDXCOLL)

print ctr, 'records inserted into database'



