import re
from VitalConstants import *
from MongoInput import *
from MongoWrite import *
import json

'''
Functions to provide utility to other modules
'''

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
    url1 = url
    if url[0]=='?':
        if parent[-1]=='/':
            return parent+url
        return parent + '/' + url

    elif url[0] == '#':
        return parent+url
    elif len(url) == 1 and url[0]=='/':
        loc = findSlashes(parent)
        return parent[:loc[0]+1]
    else:
        levelsUp = url.count('../')+1
        while url.startswith('../'):
            url = url[3:]            
        if parent.count('/')==0:
            parent+='/'

        levelsUp = min(levelsUp, parent.count('/')) # ??
        loc = findSlashes(parent)
        '''
        if len(loc) == 0:
            loc.append(len(parent)-1)
            parent+='/'
            '''

        try:
            ans = parent[:loc[len(loc)-levelsUp]+1] + url
            return ans
        except IndexError:
            print loc
            print parent
            print url1
            print levelsUp


'''
If URL contains an 'a href' or a 'mailto' or points to a non webpage resource, return False
'''
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
    

def writeSnippetsToDatabase():
    j = json_provider()
    client = createConnection()
    db = selectDatabase(client, DBNAME)
    print 'Loading complete'
    ctr=0
    for url in j.urls[1:]:
        data_dict = j.html_dict[url]
        body = data_dict['body']
        body = body.split()
        body = ' '.join(body)

        newdic = {'url':url}
        newdic['body']=body

        insertDocument(db, newdic, SNIPPETS_COLL)
        ctr+=1
        print ctr

ctr=0
anchorset = {}
