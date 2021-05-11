import flask
from flask import request
from bs4 import BeautifulSoup
import requests
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/books/details', methods=['GET'])
def api_url_v1():
    if 'url' in request.args:
        url = request.args['url']
        html = requests.get(url)

        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        soup = BeautifulSoup(html.content,'html.parser')
        rows = soup.find_all('div')

        # Create an empty dictionary for our results
        info = {}
        # Loop through the data and match results that fit the requested url.        
        for index in range(len(rows)):
            if index < 40:
                continue
            row = rows[index]
            str_rows = str(row)
            if "box-chap box-chap" in str_rows:
                cleantext = BeautifulSoup(str_rows, "lxml").get_text()    
                info['full_info'] = cleantext
                break

        title = soup.find_all('h2')
        cleanTitle = BeautifulSoup(str(title[0]), "lxml").get_text()
        info['title'] = cleanTitle
        return json.dumps(info)
    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/api/v1/books', methods=['GET'])
def api_books_url_v1():
    if 'url' in request.args:
        info = {}
        url = request.args['url']
        html = requests.get(url)

        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        soup = BeautifulSoup(html.content,'html.parser')
        bookImg = soup.find_all('a',attrs ={"id":"bookImg"})
        info['img_url'] = bookImg[0].find('img')['src']

        bookInfo = soup.find_all('h1')
        info['book_info'] = bookInfo[0].get_text()

        bookId = soup.find_all('meta', attrs ={"name":"book_detail"})
        hiddenId = bookId[0]['content']
        info['chapter_name'] = []
        info['link'] = []
        info['season'] = []
        info['season_index'] = []
        firstSeason = soup.find_all('li', attrs ={"class":"divider-chap"})
        cleanFirstSeason = BeautifulSoup(str(firstSeason[0]), "lxml").get_text()
        info['season'].append(cleanFirstSeason)
        info['season_index'].append(0)
        
        pagingUrl = "https://truyen.tangthuvien.vn/doc-truyen/page/" + hiddenId + "?page=0&limit=18446744073709551615&web=1"
        htmlTest = requests.get(pagingUrl)
        soupTest = BeautifulSoup(htmlTest.content,'html.parser')

        rowTest = soupTest.find_all('ul')
        chapters = rowTest[0].find_all('li')

        for chap in chapters:
            try:
                info['chapter_name'].append(chap.find_all('a')[0]['title'])
                info['chapter_link'].append(chap.find_all('a')[0]['href'])
            except:
                season = chap.find_all('span')
                cleanSeason = BeautifulSoup(str(season[0]), "lxml").get_text()
                if info['season'][len(info['season']) - 1][:8] == cleanSeason[:8]:
                    continue
                info['season'].append(cleanSeason)
                info['season_index'].append(len(info['chapter_name']))

        # https://truyen.tangthuvien.vn/doc-truyen/page/31803?page=1&limit=75&web=1
        return json.dumps(info)
    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/api/v2/books/details', methods=['GET'])
def api_url_v2():
    if 'url' in request.args:
        url = request.args['url']
        html = requests.get(url)

        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}

        # Find chapter title and book title container
        chapter_title = soup.find('h2')
        clean_chapter_title = BeautifulSoup(str(chapter_title), "lxml").get_text()

        book_title = soup.find('h1', attrs={"class":"truyen-title"}).find('a')['title']
        clean_book_title = BeautifulSoup(str(book_title), "lxml").get_text()

        info['book_title'] = clean_book_title
        info['chapter_title'] = clean_chapter_title

        rows = soup.find_all('div')

        # Loop through the data and match results that fit the requested url.        
        for index in range(len(rows)):
            if index < 40:
                continue
            row = rows[index]
            str_rows = str(row)
            if "box-chap box-chap" in str_rows:
                clean_text = BeautifulSoup(str_rows, "lxml").get_text()    
                info['content'] = clean_text
                break

        return json.dumps(info)
    else:
        return "Error: No url field provided. Please specify an url."

@app.route('/api/v2/books', methods=['GET'])
def api_books_url_v2():
    if 'url' in request.args:
        info = {}
        url = request.args['url']
        html = requests.get(url)

        # Check if an ID was provided as part of the URL.
        # If ID is provided, assign it to a variable.
        # If no ID is provided, display an error in the browser.
        soup = BeautifulSoup(html.content,'html.parser')

        # Find book cover image container
        book_img = soup.find('a',attrs ={"id":"bookImg"})
        info['img_url'] = book_img.find('img')['src']

        # Find book name, book info and book author container
        book_name = soup.find('h1')
        info['book_name'] = BeautifulSoup(str(book_name), "lxml").get_text()
        info['book_intro'] = soup.find('div', attrs ={'class':'book-intro'}).find('p').get_text()
        info['book_author'] = soup.find('div', attrs ={'id':'authorId'}).find('p').get_text()

        # Create lists to store multiple chapters and seasons
        info['chapter_name'] = []
        info['chapter_link'] = []
        info['season_name'] = []
        info['season_index'] = []

        # find first season container
        first_season = soup.find('li', attrs ={"class":"divider-chap"})
        clean_first_season = BeautifulSoup(str(first_season), "lxml").get_text()
        info['season_name'].append(clean_first_season)
        info['season_index'].append(0)
        
        # find chapters and seasons container
        book_id = soup.find('meta', attrs ={"name":"book_detail"})
        hidden_id = book_id['content']
        hidden_url = "https://truyen.tangthuvien.vn/doc-truyen/page/" + hidden_id + "?page=0&limit=18446744073709551615&web=1"
        hidden_html = requests.get(hidden_url)
        hidden_soup = BeautifulSoup(hidden_html.content,'html.parser')

        chapters = hidden_soup.find('ul').find_all('li')
        for chap in chapters:
            try:
                info['chapter_name'].append(chap.find('a')['title'])
                info['chapter_link'].append(chap.find('a')['href'])
            except:
                season = chap.find('span')
                clean_season = BeautifulSoup(str(season), "lxml").get_text()
                if info['season_name'][len(info['season_name']) - 1][:8] == clean_season[:8]:
                    continue
                info['season_name'].append(clean_season)
                info['season_index'].append(len(info['chapter_name']))

        info['season_index'].append(len(info['chapter_name']))

        return json.dumps(info)
    else:
        return "Error: No url field provided. Please specify an url."
        
app.run()