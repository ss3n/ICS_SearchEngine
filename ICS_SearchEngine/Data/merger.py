import cPickle as pickle
from bs4 import BeautifulSoup

def get_anchors(soup):

    anchors = soup.find_all('a')
    for i in xrange(len(anchors)):
        if anchors[i].has_attr('href'):
            href = anchors[i]['href'].encode('ascii', 'replace')
            if len(href)!= 0 and href[0] == '/':
                href = url+href
        else:
            href = ''

        text = anchors[i].text.encode('ascii', 'replace')
        anchors[i] = [href, text]
        #anchors[i] = text
    return anchors

def get_headings(soup):

    head = ''

    if soup.title and soup.title.string:
        head = soup.title.string.encode('ascii', 'replace')

    for i in xrange(1,7):
        headings = soup.find_all('h'+str(i))
        for heading in headings:
            heading = heading.get_text()
            if len(heading)>0:
                heading = heading.encode('ascii', 'replace')
                head += ' ' + heading

    headings = soup.find_all('strong')
    for heading in headings:
        heading = heading.get_text()
        if len(heading):
            heading = heading.encode('ascii', 'replace')
            head += ' ' + heading

    return head


delim = '....swarun...,,,,,arjun,,,....shiladitya....'

html_dict = {}

cntr = 0

for i in xrange(5):

    f = open('out2'+str(i+1)+'.pkl', 'r')
    pkl = f.read().split(delim)
    f.close()

    for j in xrange(len(pkl)-1):
        cntr += 1

        p_obj = pickle.loads(pkl[j])

        url = p_obj['url']
        url = url.encode('ascii', 'replace')

        if url not in html_dict:
            html = p_obj['html']
            soup = BeautifulSoup(html, 'lxml')

            text = soup.get_text().encode('ascii', 'replace')
            head = get_headings(soup)
            anchors = get_anchors(soup)

            data_dict = {}
            data_dict['head'] = head
            data_dict['body'] = text
            data_dict['anchors'] = anchors

            html_dict[url] = data_dict

        if(cntr%1000 == 0):
            print cntr, 'documents read'

print cntr, 'documents read'
f = open('out.pkl', 'w')
pickle.dump(html_dict, f)
f.close()