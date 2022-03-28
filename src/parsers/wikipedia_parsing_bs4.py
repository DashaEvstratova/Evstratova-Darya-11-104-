"""
get values from wiki site with bs4
"""

import requests
from bs4 import BeautifulSoup
from src.hash_map import HashMap

WIKI_RANDOM = 'https://ru.wikipedia.org/wiki/Special:Random'
WIKI_DOMAIN = "https://ru.wikipedia.org"

response = requests.get(WIKI_RANDOM)
soup = BeautifulSoup(response.text, 'lxml')
urls = soup.find_all('a')
link_wiki =[]
for elem in urls:
    link = elem.get("href")
    if link is not None and '/wiki/' in link:
        link_wiki.append(WIKI_DOMAIN + link)

text= soup.find('div', class_ = "mw-parser-output")
text = text.text
words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split())))
for elem in words:
    HashMap[elem] = 1
    print(HashMap())
