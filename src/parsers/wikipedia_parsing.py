"""
get values from wiki site
"""
import os.path
import time
from typing import List
from concurrent.futures import ThreadPoolExecutor
from wikipedia_parsing_bs4 import get_byte, soup_of_code, put_text, get_urls, WIKI_RANDOM, PATH
from src.maps.tree_map import TreeMap


def wiki_parser(url: str, base_path: str, map_type: type = TreeMap, number=0) -> List[str]:
    """method from url to file"""
    working_path = base_path + '/url'
    if not os.path.exists(working_path):
        os.mkdir(working_path)

    page_path = working_path + '/' + f'page_{number}'
    if not os.path.exists(page_path):
        os.mkdir(page_path)

    if not os.path.exists(page_path + '/content.xml'):
        byte_code = get_byte(url)
        with open(page_path + '/content.xml', 'wb') as file:
            file.write(byte_code)
    else:
        with open(page_path + '/content.xml', 'rb') as file:
            byte_code = file.read()

    soup = soup_of_code(byte_code)
    data = put_text(soup, map_type)
    data.write(page_path + '/words.txt')

    new_urls = get_urls(soup)
    return new_urls


def parse_depth(url: str, path: str, depth=2):
    urls = set(wiki_parser(url, path))
    new_urls = []
    page_number = 1
    for _ in range(depth - 1):
        with ThreadPoolExecutor(4) as thread:
            for new_url in urls:
                new_urls += thread.submit(wiki_parser, new_url, path, number=page_number).result()
                page_number += 1
            urls = set(new_urls) - urls


if __name__ == "__main__":
    start = time.time()
    parse_depth(WIKI_RANDOM, PATH)
    print(time.time() - start)
