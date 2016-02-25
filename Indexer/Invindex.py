# API gives a dictioary named xyz with URL name as key and dictionary {word:frequency} of words with frequency
# imp_words is a list of special words with stop words removed
# wordsinDocs is a dictionary containing word as key and a dictionary of URL names:freq containig that word

# def invertedIndex(xyz,imp_words[]):
# 	wordsinDocs={}
# 	for word in imp_words: #traverse through each word
# 		for document in xyz: #traverse through each document and check for the word  
# 			if word in value of document:  #traverse through the dictionary containing word entries inside that URL 
# 				wordsinDocs[word]+=document

# #Swarun's version

# 	for doc in documents:
# 		for word in doc:
# 			if word is already there in wordDictionary:
# 				wordDictionary[urls] += url
# 			else:
# 				wordDictionary[urls] = url

###########
## FINAL ##
###########

#Arjun's modification of swarun's version
from numpy import log10 as log

def invertedIndex(xyz):
	wordsinDocs = {}

	N = len(xyz)

	for url,doc in xyz:
		for word, count in doc:
			# if word is in wordsinDocs:
			# 	#wordsinDocs[word] += url
			# 	wordsinDocs[word][url] = count
			# else:
			# 	wordsinDocs[word] = {}
			# 	wordsinDocs[word][url] = count
			if word not in wordsinDocs:
				wordsinDocs[word] = {}

			wordsinDocs[word][url] = count

	for word, docs in wordsinDocs:
		df = len(docs)

		for url in docs.keys():
			tf = docs[url]
			docs[url] = (1.0 + log(tf))*log(N/df)

	return wordsinDocs