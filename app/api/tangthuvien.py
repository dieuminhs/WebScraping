from flask import request
from bs4 import BeautifulSoup
import requests
import json

def api_url_v1(html):
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'url' in request.args:
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

def api_books_url_v1(html):
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'url' in request.args:
        soup = BeautifulSoup(html.content,'html.parser')

        # Create an empty dictionary for our results
        info = {}

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
                info['chapter'].append(chap.find_all('a')[0]['href'])
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

def api_books_contents(url):
    html = requests.get(url)    
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}
    info['source'] = 'truyen.tangthuvien.vn'

    # Find chapter title and book title container
    info['book_title'] = soup.find('h1', attrs={"class":"truyen-title"}).find('a')['title']   
    info['chapter_title'] = soup.find('h2').get_text()

    rows = soup.find_all('div')

    # Loop through the data and match results that fit the requested url.        
    for index in range(len(rows)):
        if index < 40:
            continue
        row = rows[index]
        if "box-chap box-chap" in str(row):
            info['content'] = row.get_text()
            break

    with open('book_details_data.txt', 'w') as outfile:
        json.dump(info, outfile)  
              
    return json.dumps(info)

def api_books(url):
    html = requests.get(url)    
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}

    # Add book source
    info['source'] = 'truyen.tangthuvien.vn'

    # Find book id container    
    book_id = soup.find('meta', attrs ={"name":"book_detail"})['content']
    info['book_id'] = book_id

    # Find book cover image container
    info['img_url'] = soup.find('a', attrs ={"id":"bookImg"}).find('img')['src']

    # Find book name, book info and book author container
    info['book_name'] = soup.find('h1').get_text()
    info['book_author'] = soup.find('div', attrs ={'id':'authorId'}).find('p').get_text()    
    info['book_intro'] = soup.find('div', attrs ={'class':'book-intro'}).find('p').get_text()

    # Create lists to store multiple chapters and seasons
    info['chapter_name'] = []
    info['chapter_link'] = []
    info['season_name'] = []
    info['season_index'] = []

    # Find first season container
    info['season_name'].append(soup.find('li', attrs ={"class":"divider-chap"}).get_text())
    info['season_index'].append(0)
    
    # Find chapters and seasons container
    hidden_url = "https://truyen.tangthuvien.vn/doc-truyen/page/" + book_id + "?page=0&limit=18446744073709551615&web=1"
    hidden_html = requests.get(hidden_url)
    hidden_soup = BeautifulSoup(hidden_html.content, 'html.parser')
    chapters = hidden_soup.find('ul').find_all('li')

    # Loop through chapters list to push chapters and seasons into container list
    for chap in chapters:
        try:
            info['chapter_name'].append(chap.find('a')['title'])
            info['chapter_link'].append(chap.find('a')['href'])
        except:
            season = chap.find('span').get_text()
            if info['season_name'][len(info['season_name']) - 1][:8] == season[:8]:
                continue
            info['season_name'].append(season)
            info['season_index'].append(len(info['chapter_name']))

    info['season_index'].append(len(info['chapter_name']))
    with open('book_data.txt', 'w') as outfile:
        json.dump(info, outfile)        

    return json.dumps(info)

