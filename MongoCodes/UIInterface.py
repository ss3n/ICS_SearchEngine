from pymongo import MongoClient
from MongoWrite import *
import operator

client = createConnection()
db = selectDatabase(client)
coll = db['invIX']

# word1="machine"
# word2="learning"

word_list = [['machine', 'learning'], ['mondego'], ['security'], ['student','affairs'], ['graduate','courses'], ['computer', 'games'], ['retrieval'], ['crista', 'lopes'], ['rest'], ['software', 'engineering']]

for words in word_list:
    N = len(words)
    word1 = words[0]
    if(N==2):
        word2 = words[1]

    if N==2:
        doc = coll.find({"word":word1})[0]
        data1=doc['scores']
        # print len(data1)

        doc = coll.find({"word":word2})[0]
        data2=doc['scores']
        # print len(data2)

        # print len(data1), len(data2)
        inter = []
        inter = [i for i in data1.keys() if i in data2.keys()]
    else:
        doc = coll.find({"word":word1})[0]
        data1=doc['scores']
        inter = data1.keys()
        data2={i:0 for i in data1.keys()}

    # print len(inter)
    print words
    rankings = {i:(data1[i]+data2[i]) for i in inter}
    sorted_x = sorted(rankings.items(), key=operator.itemgetter(1), reverse=True)

    for i in sorted_x[:10]:
        a,b = i
        print a