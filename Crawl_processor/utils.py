import re
from collections import Counter
from nltk.corpus import words


###################
# Tokenizer class #
###################

class tokenizer:
	""" Class for tokenizer objects responsible for parsing a file into list of alphanumeric tokens"""

	def __init__(self):
		self.pattern = re.compile(r'[A-Za-z0-9\'\-]+')


	def tokenizeFile(self, textFile):
		""" function takes as input an open text file and returns as output a list of tokens.
			Tokens are parsed from file as alphanumeric series of characters """

		fileString = textFile.read()
		#fileString = fileString.replace('-', ' ')

		tokenList = self.pattern.findall(fileString)

		for i in xrange(len(tokenList)):
			tokenList[i] = str.lower(tokenList[i])

		return tokenList


	def print_Tokens(self, tokenList):

		print('\n'.join(tokenList))


####################
# Word frequencies #
####################

def computeWordFrequencies(tokenList):
	""" Given a list of tokens, returns a Counter object for token-count pair in token list """

	return Counter(tokenList)


def print_Frequencies(tokenCounter):
	""" Prints <token, count> pairs in descending order of count """

	sorted_count = tokenCounter.most_common()

	for t in sorted_count:
		print t[0],':',t[1]


###########
# 3-grams #
###########

def getThreeGrams(tokenList):
	gram_3_list = [];
	
	for i in xrange(len(tokenList) - 2):
		gram_3_list += [ (tokenList[i], tokenList[i+1], tokenList[i+2]) ]

	return gram_3_list


def computeThreeGramFrequencies(tokenList):
	""" Given a list of tokens, returns a Counter object for 3-gram - count pair in token list """

	gram_3_list = [];

	for i in xrange(len(tokenList) - 2):
		gram_3_list += [ (tokenList[i], tokenList[i+1], tokenList[i+2]) ]

	return Counter(gram_3_list)


def print_3GramFrequencies(gram3_Counter):
	""" Prints <3Gram, count> pairs in descending order of count """

	sorted_count = gram3_Counter.most_common()

	for t in sorted_count:
		print t[0], ':', t[1]


###########
# 2-grams #
###########

def getTwoGrams(tokenList):
	gram_2_list = [];
	
	for i in xrange(len(tokenList) - 1):
		gram_2_list += [ (tokenList[i], tokenList[i+1]) ]

	return gram_2_list


def computeTwoGramFrequencies(tokenList):
	""" Given a list of tokens, returns a Counter object for 2-gram - count pair in token list """

	gram_2_list = [];

	for i in xrange(len(tokenList) - 1):
		gram_2_list += [ (tokenList[i], tokenList[i+1]) ]

	return Counter(gram_2_list)


def print_2GramFrequencies(gram2_Counter):
	""" Prints <2Gram, count> pairs in descending order of count """

	sorted_count = gram2_Counter.most_common()

	for t in sorted_count:
		print t[0], ':', t[1]



############
# Anagrams #
############

def get_alphaCount(token):

	alpha_count = 26*[0]

	for alpha in token:
		#print token
		alpha_count[ord(alpha) - ord('a')] += 1

	return str(alpha_count)


class anagrammer:

	def __init__(self):

		self.dict_anagrams = {}

		for t in words.words():
			word = str.lower(str(t))
			word = word.replace('-',' ')

			alpha_count = get_alphaCount(word)

			if alpha_count in self.dict_anagrams:
				self.dict_anagrams[alpha_count].add(word)
			else:
				self.dict_anagrams[alpha_count] = {word}

	
	def detectAnagrams(self, tokenList):
		""" Given a list of tokens, returns a dictionary of token-anagram pair """

		anagram_list = {}

		for token in tokenList:
			if token.isalpha():
				alpha_count = get_alphaCount(token)

				if alpha_count in self.dict_anagrams:
					anagram_list[token] = list(self.dict_anagrams[alpha_count] - {token})
				else:
					anagram_list[token] = []
			
			else:
				anagram_list[token] = []

		return anagram_list


	def print_Anagrams(self, anagramList):
		""" Given a dictionary of token: <anagram-list>, print them """

		tokenList = sorted(anagramList.keys())

		for token in tokenList:
			print token, ':', anagramList[token]