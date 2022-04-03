"""
get values from wiki site with bs4
"""

import requests
from bs4 import BeautifulSoup


WIKI_RANDOM = 'https://ru.wikipedia.org/wiki/Special:Random'
WIKI_DOMAIN = "https://ru.wikipedia.org"

def get_byte(url):
    """
    mothod to get byte_code
    """
    response = requests.get(url)
    code = response.content
    return code

def soup_of_code(code):
    """
    method get html cod
    """
    soup = BeautifulSoup(code, 'lxml')
    return soup

def all_utl(soup):
    """
    get all url
    """
    urls = soup.find_all('a')
    link_wiki =[]
    size = 0
    for elem in urls:
        link = elem.get("href")
        if link is not None and '/wiki/' in link and size < 11:
            link_wiki.append(WIKI_DOMAIN + link)
            size+=1
    return link_wiki



def put_text(soup, data_cls):
    """
    put words and count them
    """
    text= soup.find('div', class_ = "mw-parser-output")
    if text is None:
        return {}
    text = text.text
    words= list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split())))
    for elem in words:
        if elem in data_cls:
            data_cls[elem] = data_cls[elem] + 1
        else:
            data_cls[elem] = 1
    return data_cls
