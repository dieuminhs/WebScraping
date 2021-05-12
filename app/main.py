import os
import sys
import flask
from flask import request
sys.path.append("Webscraping/app/api")

import tangthuvien as ttv
import truyenchu as tc
import sstruyen as sst
import truyenplus as tp

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/books', methods=['GET'])
def app_books_url():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'url' in request.args:
        url = request.args['url']

        if 'truyen.tangthuvien.vn' in url:
            module = ttv
        elif 'truyenchu.vn' in url:
            module = tc
        elif 'sstruyen.com' in url:
            module = sst
        elif 'truyenplus.vn' in url:
            module = tp

        return module.api_books(url)

@app.route('/api/books/details', methods=['GET'])
def app_url():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.    
    if 'url' in request.args:
        url = request.args['url']

        if 'truyen.tangthuvien.vn' in url:
            module = ttv
        elif 'truyenchu.vn' in url:
            module = tc
        elif 'sstruyen.com' in url:
            module = sst
        elif 'truyenplus.vn' in url:
            module = tp

        return module.api_books_details(url)

    else:
        return "Error: No url field provided. Please specify an url."
