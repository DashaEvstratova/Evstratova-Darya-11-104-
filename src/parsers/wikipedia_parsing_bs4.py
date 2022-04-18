"""
get values from wiki site with bs4
"""

import requests
from bs4 import BeautifulSoup
from validators import url as valid_url

WIKI_RANDOM = 'https://ru.wikipedia.org/wiki/Special:Random'
WIKI_DOMAIN = "https://ru.wikipedia.org"
PATH = r'C:/Users/dasha/PycharmProjects/Evstratova-Darya-11-104'


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


def get_urls(soup):
    """
    get all url
    """
    new_soup = soup.select('div[class=mw-parser-output]')
    if len(new_soup) == 0:
        return []
    urls = new_soup[0].findAll('a')
    link_wiki = []
    for elem in urls:
        link = str(elem.get("href"))
        if '/wiki/' in link:
            url = WIKI_DOMAIN + link
            if valid_url(url):
                link_wiki.append(url)
    return link_wiki


def put_text(soup, data_cls):
    """
    put words and count them
    """
    data = data_cls()
    text = soup.find('div', class_="mw-parser-output")
    if text is None:
        return {}
    text = text.text
    words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split())))
    for elem in words:
        if elem in data:
            data[elem] = data[elem] + 1
        else:
            data[elem] = 1
    return data


if __name__ == "__main__":
    print(get_urls(soup_of_code(get_byte(WIKI_RANDOM))))

