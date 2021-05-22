from flask import request
from bs4 import BeautifulSoup
import grequests
import requests
import json

# import time
# import aiohttp
# import asyncio
# import os

# from aiohttp import ClientSession

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

def async_books_contents(html):    
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

    return json.dumps(info)

def exception_handler(request, exception):
    print("Request failed")

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

    return json.dumps(info)

def async_api_books(url):
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

    info['chapter_contents'] = [None] * len(info['chapter_link'])
    htmls = []

    # for i in range(0, len(info['chapter_link']), 5):
    #     rs = (grequests.get(link) for link in info['chapter_link'][i:i+5])
    #     htmls.extend(grequests.map(rs, exception_handler=exception_handler))
    #     time.sleep(0.1)

    rs = (grequests.get(link) for link in info['chapter_link'])
    htmls.extend(grequests.map(rs, exception_handler = exception_handler))

    while True:
        request_again = [[], []]
        for idx, html in enumerate(htmls):
            if html.status_code == 503:
                request_again[0].append(info['chapter_link'][idx])
                request_again[1].append(idx)
                 
        if len(request_again[0]) == 0:
            break    

        rs = (grequests.get(link) for link in request_again[0])
        htmls_again = grequests.map(rs, exception_handler = exception_handler)
        for idx_again, html_again in enumerate(htmls_again):
            htmls[request_again[1][idx_again]] = html_again

    for idx, html in enumerate(htmls):
        print(idx)
        info['chapter_contents'][idx] = async_books_contents(html)

    return json.dumps(info)

