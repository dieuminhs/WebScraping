import flask
from flask import request
from bs4 import BeautifulSoup
import requests
import json
import urllib

def api_books_details(url):
    html = requests.get(url)        
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}

    # Find chapter title and book title container
    book_title = soup.find('h1', attrs={"class":"story-title"}).find('a')['title']
    chapter_title = soup.find('span', attrs={'class':'chapter-text'}).get_text()

    info['book_title'] = book_title
    info['chapter_title'] = chapter_title
    info['content'] = ""

    contents = soup.find('div', attrs ={'id':'chapter-c'}).find_all('p')

    # Loop through the data and match results that fit the requested url.        
    for content in contents:
        info['content'] += (content.get_text()) + '\n'
              
    return json.dumps(info)

def api_books(url):
    html = requests.get(url)    
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}

    # "Domain name to access data"
    domain = 'https://truyenchu.vn'

    # Find book cover image container
    info['img_url'] = domain + soup.find('div', attrs ={'class':'book'}).find('img')['src']

    # Find book name, book info and book author container
    info['book_name'] = soup.find('h1').find('a').get_text()
    info['book_intro'] = ""
    book_intros = soup.find('div', attrs ={'class':'desc-text'}).find_all('p')
    for book_intro in book_intros:
        info['book_intro'] += book_intro.get_text() + '\n'

    info['book_author'] = soup.find('div', attrs ={'itemprop':'author'}).find('a')['title']

    # Create lists to store multiple chapters
    info['chapter_name'] = []
    info['chapter_link'] = []
    info['season_name'] = []
    info['season_index'] = []
    
    # Find chapters container
    count = 1
    book_id = soup.find('input', attrs ={'id':'truyen-id'})['value']
    while True:
        paging_url = 'https://truyenchu.vn/api/services/list-chapter?type=list_chapter&tid=' + str(book_id) + '&page=' + str(count)
        paging_html = requests.get(paging_url)
        json_contents = paging_html.json()
        contents = BeautifulSoup(json_contents['chap_list'], 'lxml')

        # Loop through chapters list to push chapters into container list
        chapters = contents.find_all('a')
        if len(chapters) == 0:
            break
        for chap in chapters:
            info['chapter_name'].append(chap.get_text())
            info['chapter_link'].append(domain + chap['href'])
        count += 1

    return json.dumps(info)

