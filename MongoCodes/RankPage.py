from __future__ import division 
from VitalConstants import *
from MongoWrite import createConnection, selectDatabase

DAMPING = 0.85
d = DAMPING 
THRESHOLD = 0.1

def stable(currentPageRank, pastPageRank): 
    diff = [abs(currentPageRank[i] - pastPageRank[i]) for i in pastPageRank.keys()] 
    if max(diff) < THRESHOLD: 
        return True 
    return False

client = createConnection()
db = selectDatabase(client, DBNAME)
coll = db[FWDIDXCOLL]


'''
Returns a dictionary of outgoing links
outoing [<url] = <no of outgoing links> 

Example:
Where url -> url1, url2, url3
outgoing[url] = 3

Returns a dictionary of backlinks
incoming [ <url> ] = [url1, url2, url3] 

Example:
incoming ['google.com'] = ['yahoo.com', 'bing.com', 'aol.com']
where Yahoo, Bing & Aol point to Google.com
'''
def obtainIncomingAndOutgoingLinks():
    outgoing = {}
    incoming = {}

    ctr=0
    cursor = coll.find()
    for doc in cursor: #For each document in the collection
        url = doc[URL_DICT_KEY]     #Obtain URL from the document

        #If the document does not have the anchortext attribute at all, then it has no incoming or outgoing links
        if ANCHORS_DICT_KEY in doc[CONTENT_DICT_KEY]    :
            # Obtain the incoming & Outgoing dictionaries
            out = doc[CONTENT_DICT_KEY][ANCHORS_DICT_KEY][ANCHORS_OUTGOING_DICT_KEY]
            inc = doc[CONTENT_DICT_KEY][ANCHORS_DICT_KEY][ANCHORS_INCOMING_DICT_KEY]
            #TODO : Incoming set of URLS is missing. Use outgoing to add to outgoing dir
            break
            if inc!= []:
                inc = inc[0][1]

            #If either inc or out is empty, initialize the appropriate dictionaries with empty lists or length=0
            if out == []:
                outgoing[url] = 0
            else:
                outgoing[url] = len(out)

            if inc == []:
                incoming[url]=[]
            else:
                incoming[url] = inc.keys()
        else: # Case where there are no Incoming or Outgoing links
            outgoing[url] = 0
            incoming[url] = []
        ctr+=1
        if ctr%1000 == 0:
            print ctr
    print 'Reading everything Done'
    return incoming, outgoing



incoming, outgoing = obtainIncomingAndOutgoingLinks()

''' for each element in corpus: PR(A) = (1-d) + sigma(PR(Ci) / T(Ci) ''' 

def writePageRanksToDatabase(pageranks):
    ctr=1
    for url, pagerank in pageranks.iteritems():
        insert = {url:pagerank}
        insertDocument(db, insert, PAGERANK_COLL)
        ctr+=1

        if ctr%1000 == 0:
            print ctr
    print ctr, ' urls inserted into PageRank Collection'



def main():
    print '\n\nBeginning Main'
    currentPageRank = {i:1 for i in incoming.keys()}
    pastPageRank = {i:0 for i in incoming.keys()}

    it = 0

    # while not stable(currentPageRank, pastPageRank):
    #     pastPageRank = currentPageRank.copy()
    #     for page in incoming.keys():
            # print it, page, incoming[page]
            # currentPageRank[page] = (1-d)
            # try:
            #     some = [pastPageRank[i]/outgoing[i] if outgoing[i]>0 else 0 for i in incoming[page]]
            # except KeyError:
            #     print 'Debugging'
            #     print page
            #     print incoming[page]
            #     print pastPageRank[i]
            #     print outgoing[i]
            #     print currentPageRank[page]
            #     print
            #     break
            # currentPageRank[page]+=d*sum(some)
        # it +=1
        # print 'Iteration #', it
 
    for page in incoming.keys():
        if incoming[page] != []:
            print page
            print incoming[page]
            print

    # print currentPageRank 
    # writePageRanksToDatabase(currentPageRank)
main()
