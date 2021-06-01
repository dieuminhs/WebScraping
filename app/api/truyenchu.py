from bs4 import BeautifulSoup
import requests
import json
import asyncio
import aiohttp

def api_books_contents(url):
    html = requests.get(url)        
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}
    info['source'] = 'truyenchu.vn'
    
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

    # Add book source    
    info['source'] = 'truyenchu.vn'

    # Find book id container    
    book_id = soup.find('input', attrs ={'id':'truyen-id'})['value']
    info['book_id'] = book_id

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

def async_books_contents(soup):
    # Create an empty dictionary for our results
    info = {}
    info['source'] = 'truyenchu.vn'
    
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

async def get(semaphore, url, session, timeout=10):
    try:
        async with semaphore:
            # with async_timeout.timeout(timeout):
                async with session.get(url=url) as response:
                    
                    resp = await response.read()
                    soup = BeautifulSoup(resp.decode('utf-8'), 'html5lib')

                    return soup
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def get_chapters(urls):
    sem = asyncio.Semaphore(1)
    
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(sem, url, session) for url in urls])
    return ret         

def async_api_books(url):
    html = requests.get(url)    
    soup = BeautifulSoup(html.content,'html.parser')

    # Create an empty dictionary for our results
    info = {}

    # Add book source    
    info['source'] = 'truyenchu.vn'

    # Find book id container    
    book_id = soup.find('input', attrs ={'id':'truyen-id'})['value']
    info['book_id'] = book_id

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

    info['chapter_contents'] = [None] * len(info['chapter_link'])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    soups = loop.run_until_complete(get_chapters(info['chapter_link']))
    # end = time.time()
    # print(end-start)
    
    for idx, soup in enumerate(soups):
        info['chapter_contents'][idx] = async_books_contents(soup)        

    return json.dumps(info)
