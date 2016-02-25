import cPickle as pickle
from bs4 import BeautifulSoup

delim = '....swarun...,,,,,arjun,,,....shiladitya....'

html_dict = {}

for i in xrange(5):

	f = open('out2'+str(i+1)+'.pkl', 'r')
	pkl = f.read().split(delim)
	f.close()

	for j in xrange(len(pkl)-1):
		p_obj = pickle.loads(pkl[j])

		url = p_obj['url']
		url = url.encode('ascii', 'replace')

		if url not in html_dict:
			html = p_obj['html']
			soup = BeautifulSoup(html, 'lxml')

			text = soup.get_text().encode('ascii', 'replace')

			if soup.title and soup.title.string:
				head = soup.title.string.encode('ascii', 'replace')

			anchors = soup.find_all('a')
			for i in xrange(len(anchors)):
				if anchors[i].has_attr('href'):
					href = anchors[i]['href'].encode('ascii', 'replace')
					if href[0] == '/':
						href = url+href
				else:
					href = ''

				text = anchors[i].text.encode('ascii', 'replace')
				anchors[i] = [href, text]

			data_dict = {}
			data_dict['head'] = head
			data_dict['body'] = text
			data_dict['anchors'] = anchors

			html_dict[url] = data_dict

f = open('out.pkl', 'w')
pickle.dump(html_dict, f)
f.close()