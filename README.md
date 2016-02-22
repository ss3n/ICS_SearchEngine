# ICS_SearchEngine
Repository for information retrieval project to build search engine on http://www.ics.uci.edu

Crawl Data:
Link for downlaoding the crawled data in cPickle file: https://drive.google.com/folderview?id=0B9z5Pvyebk-0MDY5cm82T28yaVE&usp=sharing

Data description:

The data is stored as a Python dictionary inside the pickle file. The keys for the dictionary are urls as strings.

The value corresponding to each key is again a dictionary. This secondary dictionary has three key-value entries:

    1. key - 'head'; value - heading string
    
    2. key - 'body'; value - text body as a string
    
    3. key - 'anchors'; value - list of strings containing anchor texts
    
There are two files:
  outU8.pkl - contains all strings encoded in UTF-8
  
  out.pkl - contains all strings encoded in ASCII
