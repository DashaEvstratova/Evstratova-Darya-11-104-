"""
get values from wiki site
"""
import os.path
from urllib.request import urlopen
import re
from typing import List
from src.maps.tree_map import TreeMap

from wikipedia_parsing_bs4 import get_byte, soup_of_code, put_text, all_utl

def write_in(url:str, get_path:str, use_map, number) -> None:
    """
    method put in file
    """
    directory = 'page_' + str(number)
    if not os.path.exists(get_path +'/'+directory):
        os.mkdir(get_path + '/' + directory)
    new_path = get_path + '/' + directory

    if not os.path.exists(get_path +'/'+directory):
        byte_code = get_byte(url)
        with open(new_path + '/content.xml', 'wb') as file:
            file.write(byte_code)
    else:
        with open(new_path + '/content.xml', 'rb') as file:
            byte_code = file.read()
    soup = soup_of_code(byte_code)
    count, data = put_text(soup, use_map)
    data.write(new_path + '/words.txt')

def wiki_parser(url:str, base_path:str, map_type: type = TreeMap) -> List[str]:
    """
    method from url to file
    """
    if not os.path.exists(base_path + '/url'):
        os.mkdir(base_path + '/url')

    write_in(url, base_path + '/url', map_type, 0)
    use = '/url/page_number_0/content.xml'
    with open(base_path + use, 'r', encoding='utf-8')as file:
        new_ = all_utl(soup_of_code(file.read()))[0]
    size = all_utl(soup_of_code(file.read()))[1]
    for i in range(size):
        write_in(new_[i], base_path + '/url', map_type, i+1)
