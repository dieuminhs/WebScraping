import flask
from flask import request

import app.api.tangthuvien as ttv
import app.api.truyenchu as tc
import app.api.sstruyen as sst
import app.api.truyenplus as tp

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/books', methods=['GET'])
def book_books_url():
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

@app.route('/api/books/contents', methods=['GET'])
def books_contents_url():
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

        return module.api_books_contents(url)

    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/api/chapters', methods=['GET'])
def chapters_url():
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

        return module.api_books_contents(url)

    else:
        return "Error: No url field provided. Please specify an url."
