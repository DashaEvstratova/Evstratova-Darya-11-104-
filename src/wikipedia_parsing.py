"""
get values from wiki site
"""

from urllib.request import urlopen
import re

WIKI_RANDOM = "https://ru.wikipedia.org/wiki/Special:Random"
WIKI_DOMAIN = "https://ru.wikipedia.org"
response = urlopen(WIKI_RANDOM)
response_bytes = response.read()

txt = response_bytes.decode("utf8")
urls = re.findall(r'href=[\'"]?([^\'">]+)', txt)
filtered_urls = filter(lambda url: url.startswith('/wiki/'), urls)
corrected_urls = map(lambda url: WIKI_DOMAIN + url, filtered_urls)


words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), txt.split())))
