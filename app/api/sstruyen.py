import flask
from flask import request
from bs4 import BeautifulSoup
import requests
import json

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
    domain = 'https://sstruyen.com/'

    # Find book cover image container
    info['img_url'] = domain + soup.find('div', attrs ={'class':'book-list story-details'}).find('img')['data-src']

    # Find book name, book info and book author container
    info['book_name'] = soup.find('h1', attrs ={'class':'title'}).find('a').get_text()

    book_intros = soup.find('div', attrs ={'class':'content1'})
    for idx, book_intro in enumerate(book_intros):
        if idx == 0:
            info['book_author'] = book_intro.find('a', attrs ={'itemprop':'author'}).get_text()
        else:
            info['book_intro'] = book_intro.get_text()

    # Create lists to store multiple chapters
    info['chapter_name'] = []
    info['chapter_link'] = []

    # Find chapters container
    count = 1
    book_domain = soup.find('link')['href']
    should_continue = True

    while True:
        paging_url = book_domain + 'trang-' + str(count) + '/#s_c_content'
        paging_html = requests.get(paging_url)
        paging_soup = BeautifulSoup(paging_html.content,'html.parser')
        
        rows = paging_soup.find('div', attrs = {'class':'row list-chap'})
        if len(rows) < 5: 
            break
        for idx, row in enumerate(rows):
            if idx > 2:
                chapters = row.find_all('li')

                # Loop through chapters list to push chapters into container list    
                for chap in chapters:
                    info['chapter_name'].append(chap.find('a')['title'])
                    info['chapter_link'].append(book_domain + chap.find('a')['href'])
        count += 1

    return json.dumps(info)

