'''
Reads from the Crawler dump and sends ONE page of text contents at a time to its driver function
'''
import sys
sys.path.insert(0, '../Crawl_processor')
from utils import *

import cPickle as pickle
from cStringIO import StringIO
from collections import Counter


def rm_stop(counter):

	stop_file = open('../Crawl_processor/stop_words.txt', 'r')
	stop_list = stop_file.read().split('\n')
	stop_file.close()

	stopless_dict = {}

	for entry,count in counter.iteritems():
		if entry not in stop_list and entry.isalpha() and len(entry) <= 45:
			stopless_dict[entry] = count

	return stopless_dict


def get_count_positions(word_counter, word_list):

	word_info = {}

	for word,count in word_counter.iteritems():
		info_dict = {}
		info_dict['count'] = count
		info_dict['positions'] = []
		word_info[word] = info_dict

	for i, word in enumerate(word_list):
		if word in word_info:
			word_info[word]['positions'] += [i]

	return word_info


class json_provider:

	def __init__(self, fileName = '../Data/out100.pkl'):

		self.html_dict = pickle.load(open(fileName, 'r'))
		self.urls = self.html_dict.keys()
		self.num_pages = len(self.html_dict)
		self.current_urlIX = 0

	def getNext(self):

		if self.current_urlIX == self.num_pages:
			return {}

		url = self.urls[self.current_urlIX]
		self.current_urlIX += 1

		data_dict = self.html_dict[url]
		head = data_dict['head']
		body = data_dict['body']
		anchors = data_dict['anchors']

		t = tokenizer()

		stream = StringIO(head)
		head_list = t.tokenizeFile(stream)
		head_counter = Counter(head_list)#.most_common()
		head_counter = rm_stop(head_counter)
		head_info = get_count_positions(head_counter, head_list)

		stream = StringIO(body)
		body_list = t.tokenizeFile(stream)
		body_counter = Counter(body_list)#.most_common()
		body_counter = rm_stop(body_counter)
		body_info = get_count_positions(body_counter, body_list)

		# stream = StringIO(' '.join(anchors))
		# anchor_list = t.tokenizeFile(stream)
		# anchor_counter = Counter(anchor_list)#.most_common()
		# anchor_counter = rm_stop(anchor_counter)
		# anchor_info = get_count_positions(anchor_counter, anchor_list)

		anchor_dict = {}
		for anchor in anchors:
			link = anchor[0]
			text = anchor[1]

			stream = StringIO(text)
			anchor_list = t.tokenizeFile(stream)
			anchor_counter = Counter(anchor_list)
			anchor_counter = rm_stop(anchor_counter)
			anchor_info = get_count_positions(anchor_counter, anchor_list)

			anchor_dict[link] = anchor_info

		
		data_dict = {}
		data_dict['head'] = head_info
		data_dict['body'] = body_info
		data_dict['anchors'] = anchor_dict

		input_dict = {}
		input_dict[url] = data_dict

		return input_dict


	def reset(self):

		self.current_urlIX = 0
