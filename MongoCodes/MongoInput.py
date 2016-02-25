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

	for entry in counter:
		if entry[0] not in stop_list:
			stopless_dict[entry[0]] = entry[1]

	return stopless_dict


class json_provider:

	def __init__(self, fileName = '../Data/out.pkl'):

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
		head_counter = Counter(head_list).most_common()
		head_counter = rm_stop(head_counter)

		stream = StringIO(body)
		body_list = t.tokenizeFile(stream)
		body_counter = Counter(body_list).most_common()
		body_counter = rm_stop(body_counter)

		stream = StringIO(' '.join(anchors))
		anchor_list = t.tokenizeFile(stream)
		anchor_counter = Counter(anchor_list).most_common()
		anchor_counter = rm_stop(anchor_counter)

		data_dict = {}
		data_dict['head'] = head_counter
		data_dict['body'] = body_counter
		data_dict['anchors'] = anchor_counter

		input_dict = {}
		input_dict[url] = data_dict

		return input_dict


	def reset(self):

		self.current_urlIX = 0