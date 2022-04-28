"""get values from wiki site"""

import os.path
import time
import uuid
from typing import List
from concurrent.futures import ThreadPoolExecutor
from src.parsers.wikipedia_parsing_bs4 import get_byte, soup_of_code, put_text
from src.parsers.wikipedia_parsing_bs4 import get_urls, WIKI_RANDOM, PATH
from src.maps.tree_map import TreeMap


def wiki_parser(url: str, base_path = PATH, map_type: type = TreeMap) -> List[str]:
    """method from url to file"""
    # Директория куда будет записаны папки с обработанными ссылками
    working_path = base_path + '/url'
    # Если такой папки нет в директории
    if not os.path.exists(working_path):
        # Создаем папку для ссылок
        os.mkdir(working_path)
    # Директория куда будет записаны обработанные ссылки
    page_path = working_path + '/' + uuid.uuid4().hex
    # Если эту ссылку еще не обработали
    if not os.path.exists(page_path):
        # Создаем папку для нее
        os.mkdir(page_path)

    # Если в папке ссылки нет файла с байт кодом
    if not os.path.exists(page_path + '/content.xml'):
        # создать байт код
        byte_code = get_byte(url)
        # открыть файл для записиси байт кода
        with open(page_path + '/content.xml', 'wb') as file:
            # Записываем байт код
            file.write(byte_code)
    else:
        # В противном случае, открываем уже готовый файл с байт кодом
        with open(page_path + '/content.xml', 'rb') as file:
            # Достаем байт код
            byte_code = file.read()

    # достаем содержимое по байт коду
    soup = soup_of_code(byte_code)
    # обрабатывает слова через мапу
    data = put_text(soup, map_type)
    # Записывает результат в файлик
    data.write(page_path + '/words.txt')

    # Достаем список с вики сылками
    new_urls = get_urls(soup)
    return new_urls

def parse_depth(url: str, path: str, depth=2):
    """method parse_depth"""
    # Делаем из списка множество ссылок, чтоб убрать дубликаты
    urls = set(wiki_parser(url, path))
    next_step = []
    # Цикл для счета потоков
    for _ in range(depth - 1):
        # Создание четырех потоков одновременно
        with ThreadPoolExecutor(4) as thread:
            # Создаем список новых ссылок
            new_urls = thread.map(wiki_parser, urls)
            # Проходимся по каждой ссылки
            for new_url in new_urls:
                # Добавляем в список
                next_step += new_url
            # добавляются ссылки и удаляютсся дубликаты
            urls = set(next_step) - urls

def merging_files(path = PATH):
    '''merge all files into one'''
    # Директория, где лежат обработанные ссылки
    path = PATH + '/url/'
    # Словарь, где будут все слова будут
    data = {}
    # Достаем список названий всех папок в папке url
    with os.scandir(path) as entries:
        # Проходимся по каждой папке
        for entry in entries:
            # Прописываем путь к папке
            file_name = path + entry.name + '/words.txt'
            # Временный словарь, для записиси слов из текущей папки
            current_folder = {}
            # Читаем и записываем в словарь слова
            with open(file_name, 'r', encoding='utf8') as filen:
                line_read = filen.readline().strip().split(' ')
                while len(line_read)>1:
                    current_folder[line_read[0]] = int(line_read[1])
                    line_read = filen.readline().strip().split(' ')
                # Соединяем временный словарь с основным
                for elem, key in current_folder.items():
                    # Если такого слова еще не было, то добавляем
                    if elem not in data:
                        data[elem] = key
                    # В противном случае увеличиваем счетчик
                    else:
                        data[elem] = key + data[elem]
    # Путь, где будет хранится результат
    path = PATH+'/result.txt'
    # Записываем результат
    with open(path, 'w', encoding='utf8') as w_f:
        for key, value in data.items():
            w_f.write(str(key) + " " + str(value) + "\n")

if __name__ == "__main__":
    start = time.time()
    parse_depth(WIKI_RANDOM, PATH)
    print(time.time() - start)
    start = time.time()
    merging_files()
    print(time.time() - start)
