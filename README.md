# WebScraping
## 1/ Installation instruction:
- Install python (https://www.python.org/downloads/), check Environment Path
- Install flask, beautifulsoup4, requests, lxml (use pip install "package" in the command line)
- Run the local server using:
  + Run using command line (python api.py)
  + Run build using a code editor, tools (Visual studio code, Visual studio 20xx, Jupyter notebook)
## 2/ Local server usage:
### Version 1:
- The local server running on http://127.0.0.1:5000/
- There are currently 2 function available:
  + Get book contents in a chapter page of a book (http://127.0.0.1:5000/api/v1/books/contents?url=pageUrl)
  + e.g: http://127.0.0.1:5000/api/v1/books/details?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
  + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
    * The returned value will be in json format contains 2 keys:
      + "title": contains the chapter title
      + "full_info": to extract books content of the chapter
  + Get book details in the main page of a book (http://127.0.0.1:5000/api/v1/books?url=pageUrl)
  + e.g: http://127.0.0.1:5000/api/v1/books?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
  + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
    * The returned value will be in json format contains 6 keys:
      + "img_url": contains the url of the book cover
      + "book_info": contains the book name
      + "chapter_name": contains the list of chapter name of the book
      + "link": contains the list of chapter link correspond to the chapter_name (link[i] will be the link for chapter_name[i])
      + "season": some books will contain seasons and each season the chapter number will start over, this key will contain the list of season number and season name
      + "season_index": contains a list that indicate index of the beginning chapter of each season in chapter_name (season_index[i] will return beginning chapter index of season[i]). This means the list of chapter of season[i] will from chapter_name[season_index[i]] to chapter_name[season_index[i+1]]

### Version 2:
- The local server running on http://127.0.0.1:5000/
- There are currently 2 function available:
  + Get book contents in a chapter page of a book (http://127.0.0.1:5000/api/v2/books/contents?url=pageUrl)
  + e.g: http://127.0.0.1:5000/api/v2/books/details?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
  + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien/chuong-4
    * The returned value will be in json format contains 2 keys:
      + "book_title": contains the book title
      + "chapter_title": contains the chapter title
      + "content": contains chapter contents
  + Get book details in the main page of a book (http://127.0.0.1:5000/api/v2/books?url=pageUrl)
  + e.g: http://127.0.0.1:5000/api/v1/books?url=https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
  + pageUrl: https://truyen.tangthuvien.vn/doc-truyen/luan-hoi-nhac-vien
    * The returned value will be in json format contains 6 keys:
      + "img_url": contains the url of the book cover
      + "book_name": contains the book name
      + "book_intro": contains the book introduction
      + "book_author": contains the author name of the book
      + "chapter_name": contains the list of chapter name of the book
      + "chapter_link": contains the list of chapter link correspond to the chapter_name (link[i] will be the link for chapter_name[i])
      + "season_name": some books will contain seasons and each season the chapter number will start over, this key will contain the list of season number and season name
      + "season_index": contains a list that indicate index of the beginning chapter of each season in chapter_name (season_index[i] will return beginning chapter index of season[i]). This means the list of chapter of season[i] will from chapter_name[season_index[i]] to chapter_name[season_index[i+1]]
