from flask import Flask, Response, url_for, request
import flask
import json 
import httplib2 

app = Flask(__name__)

#Insert JSON reqponse below
'''
reqdJson is a dictionary with the only key as 'items' and values as a list of items
Each item is a dictionary itself containing : itemheading, itemURL, itemcontent
'''

reqdJson = {}
reqdJson['items'] = []
item = {}
item['itemheading'] = 'Google'
item['itemURL'] = 'http://www.google.com'
item['itemcontent'] = 'Google Mein Doodle Baby Machine Google Mein Doodle Baby Google Mein Doodle Baby learning Google Mein Doodle Baby Google Mein Doodle Baby machine Google Mein Doodle Baby Learning Google Mein Doodle Baby machine learning Google Mein Doodle Baby Google Mein Doodle Baby '
reqdJson['items'].append(item)


item = {}
item['itemheading'] = 'Bing'
item['itemURL'] = 'http://www.bing.com'
item['itemcontent'] = 'Bing LOL machine Bing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOL learning machine learning Bing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOLBing LOL'
reqdJson['items'].append(item)


#Flask Server that accepts urls of the form <url>:<portno>/query=<querystring>
#Alowas returns the same json object
@app.route('/query=<que>', methods=['POST', 'GET'])
def api_root(que):
    print request.url
    print que, 'is the query string'
    goog = request.args.get('googleresults')
    a= goog.split('`````')
    for i in a:
        print i

    return json.dumps(reqdJson)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2564)