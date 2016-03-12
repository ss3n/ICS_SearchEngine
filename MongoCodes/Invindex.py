# API gives a dictioary named xyz with URL name as key and dictionary {word:frequency} of words with frequency
# imp_words is a list of special words with stop words removed
# wordsinDocs is a dictionary containing word as key and a dictionary of URL names:freq containig that word

# def invertedIndex(xyz,imp_words[]):
#   wordsinDocs={}
#   for word in imp_words: #traverse through each word
#       for document in xyz: #traverse through each document and check for the word  
#           if word in value of document:  #traverse through the dictionary containing word entries inside that URL 
#               wordsinDocs[word]+=document

# #Swarun's version

#   for doc in documents:
#       for word in doc:
#           if word is already there in wordDictionary:
#               wordDictionary[urls] += url
#           else:
#               wordDictionary[urls] = url

###########
## FINAL ##
###########

'''
Forward Index Entry:
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
    "incoming" : [(url, textcontent)]
    "outgoing" : <outgoingurl>
}


Inverted Index Entry:
{
    "term" : <word>
    "content" : {<content>}
}

<content>[<url>]
{
    "url" : <url>
    "value" : <tf-idf value>
    "positions" : <list of positions>
}

    
'''
from numpy import log10 as log
from pymongo import MongoClient
from MongoWrite import *
from VitalConstants import *

def invertedIndex(fwd_entry):
    url = fwd_entry['url']
    content = fwd_entry['content']

    inv_body = {}
    inv_head = {}
    inv_anchor = {}

    for word, fwd_details in content['body'].iteritems():
        inv_content['url'] = url
        inv_content['value'] = fwd_details['count']
        inv_content['positions'] = fwd_details['positions']

        inv_body[word] = inv_content

    for word, fwd_details in content['head'].iteritems():
        inv_content['url'] = url
        inv_content['value'] = fwd_details['count']
        inv_content['positions'] = fwd_details['positions']

        inv_head[word] = inv_content

    for anchor_in in content['anchortext']['incoming']:
        text = anchor_in[1]
        for word, fwd_details in text.iteritems():
            inv_content['url'] = url
            inv_content['value'] = fwd_details['count']
            inv_content['positions'] = fwd_details['positions']

            inv_anchor[word] = inv_content

    return {'body': inv_body, 'head': inv_head, 'anchor': inv_anchor}


def tf(coll):
    ctr=0
    inv_body = {}
    inv_head = {}
    inv_anchor = {}

    for page in coll.find():
        ctr += 1

        page_inv = invertedIndex(page)

        page_inv_body = page_inv['body']
        page_inv_head = page_inv['head']
        page_inv_anchor = page_inv['anchor']

        for word, content in page_inv_body.iteritems():
            url = content['url']

            if word not in inv_body:
                inv_body[word] = {}
            inv_body[word][url] = content

        for word, content in page_inv_head.iteritems():
            url = content['url']

            if word not in inv_head:
                inv_head[word] = {}
            inv_head[word][url] = content

        for word, content in page_inv_anchor.iteritems():
            url = content['url']

            if word not in inv_body:
                inv_anchor[word] = {}
            inv_anchor[word][url] = content

    return [{'body': inv_body, 'head': inv_head, 'anchor': inv_anchor}, ctr]

#docs[url] = (1.0 + log(tf))*log(N/df)
def tf_idf(invIndex, N):
    inv_body = invIndex['body']
    inv_head = invIndex['head']
    inv_anchor = invIndex['anchor']

    for word, content in inv_body:
        df = len(content.keys())

        for url in content.keys():
            tf = content[url]['value']
            content[url]['value'] = (1.0 + log(tf))*log(N/df)
        inv_body[word] = content

    for word, content in inv_head:
        df = len(content.keys())

        for url in content.keys():
            tf = content[url]['value']
            content[url]['value'] = (1.0 + log(tf))*log(N/df)
        inv_head[word] = content

    for word, content in inv_anchor:
        df = len(content.keys())

        for url in content.keys():
            tf = content[url]['value']
            content[url]['value'] = (1.0 + log(tf))*log(N/df)
        inv_anchor[word] = content

    return {'body': inv_body, 'head': inv_head, 'anchor': inv_anchor}    


def write_tf_idf_to_mongo(invIndex):
    inv_body = invIndex['body']
    inv_head = invIndex['head']
    inv_anchor = invIndex['anchor']
    
    ctr=1

    for word, content in inv_body.iteritems():
        entry = {}
        entry['term'] = word
        entry['content'] = content
        insertDocument(db, entry, INVIDXCOLL+'_body')

        ctr+=1
        if ctr%1000 == 0:
            print ctr
    print ctr, 'body words inserted into MongoDB'

    ctr=1

    for word, content in inv_head.iteritems():
        entry = {}
        entry['term'] = word
        entry['content'] = content
        insertDocument(db, entry, INVIDXCOLL+'_head')

        ctr+=1
        if ctr%1000 == 0:
            print ctr
    print ctr, 'head words inserted into MongoDB'

    ctr=1

    for word, content in inv_anchor.iteritems():
        entry = {}
        entry['term'] = word
        entry['content'] = content
        insertDocument(db, entry, INVIDXCOLL+'_anchor')

        ctr+=1
        if ctr%1000 == 0:
            print ctr
    print ctr, 'anchor words inserted into MongoDB'


client=createConnection()
db = selectDatabase(client)
coll = db[FWDIDXCOLL]

invIndex, N = tf(coll)
invIndex = tf_idf(invIndex, N)
write_tf_idf_to_mongo(invIndex)

