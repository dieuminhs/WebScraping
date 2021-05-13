from bs4 import BeautifulSoup
import requests
import json

def api_books_contents(url):
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

    # Find chapters container
    count = 1
    book_domain = domain + soup.find('h1').find('a')['href']
    paging_url = 'https://truyenchu.vn/api/services/list-chapter?type=list_chapter&tid=55&tascii=thuong-thien-phach-huyet&page=4&totalp=0'
    paging_html = requests.get(paging_url)
    paging_soup = BeautifulSoup(paging_html.content,'html.parser')
     
    data = paging_html.json()
    
    for i in data['chap_list'].find_all('div'):
        print(i)
    chapters = paging_soup.find('div', attrs ={'id':'list-chapter'})
    print(chapters)

    # Loop through chapters list to push chapters into container list
    for chap in chapters:
        info['chapter_name'].append(chap.find('a').find('span').get_text())
        info['chapter_link'].append(domain + chap.find('a')['href'])

    return json.dumps(info)

