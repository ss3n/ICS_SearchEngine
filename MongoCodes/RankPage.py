from __future__ import division 
x= {} #x[3] = [4] => Page 4 has a link to 3. i.e Page 3 has a backlink from 4 
x[1] = [2, 3, 4] 
x[2] = [3, 4] 
x[3] = [4] 
x[4] = [] 

numlinks = 4 
d = 0.85 
THRESHOLD = 0.01 

outgoing = {1:0, 2:1, 3:2, 4:3} 
''' for each element in corpus: PR(A) = (1-d)/numlink + sigma(PR(Ci) / T(Ci) ''' 
def stable(currentPageRank, pastPageRank): 
    diff = [currentPageRank[i] - pastPageRank[i] for i in pastPageRank.keys()] 
    if max(diff) < THRESHOLD: 
        return True 
    return False

currentPageRank = {i:1 for i in x.keys()}
pastPageRank = {i:0 for i in x.keys()}

while not stable(currentPageRank, pastPageRank):
    pastPageRank = currentPageRank.copy()
    for page in x.keys():
        print page
        currentPageRank[page] = (1-d)/numlinks
        some = [pastPageRank[i]/outgoing[i] if outgoing[i]>0 else 0 for i in x.keys()]
        currentPageRank[page]+=sum(some)
print pastPageRank 
print currentPageRank 

