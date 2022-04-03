"""
get values from wiki site with bs4
"""

import requests
from bs4 import BeautifulSoup
from src.maps.tree_map import TreeMap

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
        if link is not None and '/wiki/' in link:
            link_wiki.append(WIKI_DOMAIN + link)
            size+=1
    return [link_wiki, size]



def put_text(soup, data_cls):
    """
    put words and count them
    """
    count = 0

    text= soup.find('div', class_ = "mw-parser-output")
    for url in text:
        url = url.text
        words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), url.split())))
        for elem in words:
            count+=1
            data_cls[elem] = 1
        return count, data_cls
