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
    working_path = ''.join([base_path, '/url'])
    # Если такой папки нет в директории
    if not os.path.exists(working_path):
        # Создаем папку для ссылок
        os.mkdir(working_path)
    # Директория куда будет записаны обработанные ссылки
    page_path = '/'.join([working_path, uuid.uuid4().hex])
    # Если эту ссылку еще не обработали
    if not os.path.exists(page_path):
        # Создаем папку для нее
        os.mkdir(page_path)

    # Если в папке ссылки нет файла с байт кодом
    if not os.path.exists(''.join([page_path, '/content.xml'])):
        # создать байт код
        byte_code = get_byte(url)
        # открыть файл для записиси байт кода
        with open(''.join([page_path, '/content.xml']), 'wb') as file:
            # Записываем байт код
            file.write(byte_code)
    else:
        # В противном случае, открываем уже готовый файл с байт кодом
        with open(''.join([page_path, '/content.xml']), 'rb') as file:
            # Достаем байт код
            byte_code = file.read()

    # достаем содержимое по байт коду
    soup = soup_of_code(byte_code)
    # обрабатывает слова через мапу
    data = put_text(soup, map_type)
    # Записывает результат в файлик
    data.write(''.join([page_path, '/words.txt']))

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
def get_file(filename):
    with open(filename) as inp:
        line = inp.readline()
        while len(line)>1:
            key, value = line.split()
            value = int(value)
            yield key, value
            line = inp.readline()

def merging(arr, start, middle, stop, buf):
    left_offset = start
    right_offset = middle+1
    buff_offset = start
    while left_offset<= middle and right_offset<=stop:
        if arr[left_offset] <= arr[right_offset]:
            buf[buff_offset] = arr[left_offset]
            left_offset+=1
        else:
            buf[buff_offset] = arr[right_offset]
            right_offset+=1
        buff_offset+=1
    for i in range(left_offset, middle+1):
        buf[buff_offset] = arr[i]
        buff_offset+=1
    for i in range(right_offset, len(arr)):
        buf[buff_offset] = arr[i]
        buff_offset+=1
    for i in range(0, len(arr)):
        arr[i] = buf[i]

def sort(arr):
    buf = [0]*len(arr)
    merge_sort(arr, 0, len(arr)-1, buf)

def merge_sort(arr, start, stop, buf):
    if start >= stop:
        return
    middle = (start + stop)//2
    merge_sort(arr, start, middle, buf)
    merge_sort(arr, middle+1, stop, buf)
    merging(arr, start, middle, stop, buf)

def merging_files(path = PATH):
    '''merge all files into one'''
    # Директория, где лежат обработанные ссылки
    path = ''.join([PATH, '/url/'])
    # Словарь, где будут все слова будут
    data = []
    # Достаем список названий всех папок в папке url
    with os.scandir(path) as entries:
        # Проходимся по каждой папке
        for entry in entries:
            # Прописываем путь к папкe
            file_name = ''.join([path, entry.name, '/words.txt'])
            # Временный словарь, для записиси слов из текущей папки
            data.append(get_file(file_name))




    #         # Читаем и записываем в словарь слова
    #         with open(file_name, 'r', encoding='utf8') as filen:
    #             line_read = filen.readline().strip().split(' ')
    #             keys_data = list(data.keys())
    #             index = 0
    #             print(len(keys_data))
    #             while len(line_read)>1:
    #                 if index < len(keys_data):
    #                     while keys_data[index] < line_read[0] and index < len(keys_data):
    #                         current_folder[keys_data[index]] = data[keys_data[index]]
    #                         index+=1
    #                     if keys_data[index] == line_read[0]:
    #                         current_folder[keys_data[index]] = data[keys_data[index]] + int(line_read[1])
    #                         index+=1
    #                     elif keys_data[index] > line_read[0] or index >= len(keys_data):
    #                         current_folder[line_read[0]] = int(line_read[1])
    #                 else:
    #                     current_folder[line_read[0]] = int(line_read[1])
    #                 line_read = filen.readline().strip().split(' ')
    #         for i in range(index, len(keys_data)):
    #             current_folder[keys_data[index]] = data[keys_data[index]]
    #         data = current_folder
    # path = PATH + '/result.txt'
    # # Записываем результат
    # with open(path, 'w', encoding='utf8') as w_f:
    #     for key, value in data.items():
    #         w_f.write(str(key) + " " + str(value) + "\n")
    #             # Соединяем временный словарь с основным
    #             if len(data) < 1:
    #                 for elem, key in current_folder.items():
    #                     # Если такого слова еще не было, то добавляем
    #                     if elem not in data:
    #                         data[elem] = key
    #                     # В противном случае увеличиваем счетчик
    #                     else:
    #                         data[elem] = key + data[elem]
    #             else:
    #                 keys_data = list(data.keys())
    #                 keys_curr = list(current_folder.keys())
    #                 res = {}
    #                 data_i = 0
    #                 curr_i = 0
    #                 print(len(data), len(current_folder))
    #                 while (data_i < len(data)) and (curr_i <len(current_folder)):
    #                     if keys_curr[curr_i] in res:
    #                         res[keys_curr[curr_i]] = current_folder[keys_curr[curr_i]] + res[keys_curr[curr_i]]
    #                         print(1)
    #                         curr_i+=1
    #                     if keys_data[data_i] in res:
    #                         res[keys_data[data_i]] = data[keys_data[data_i]] + res[keys_data[data_i]]
    #                         print(0)
    #                         data_i+=1
    #                     elif keys_data[data_i] > keys_curr[curr_i]:
    #                         res[keys_curr[curr_i]] = current_folder[keys_curr[curr_i]]
    #                         print(1)
    #                         curr_i +=1
    #                     elif keys_data[data_i] < keys_curr[curr_i]:
    #                         res[keys_data[data_i]] = data[keys_data[data_i]]
    #                         print(0)
    #                         data_i+=1
    #                 print(data_i, curr_i)
    #                 if data_i == len(data):
    #                     for _ in range(curr_i, len(current_folder)):
    #                         if keys_curr[curr_i] not in res:
    #                             res[keys_curr[curr_i]] = current_folder[keys_curr[curr_i]]
    #                         else:
    #                             res[keys_curr[curr_i]] = current_folder[keys_curr[curr_i]] + res[keys_curr[curr_i]]
    #                 else:
    #                     for _ in range(data_i, len(data)):
    #                         if keys_data[data_i] not in res:
    #                             res[keys_data[data_i]] = data[keys_data[data_i]]
    #                         else:
    #                             res[keys_data[data_i]] = data[keys_data[data_i]] + res[keys_data[data_i]]
    #                 data = res.copy()
    #                 print(data)
    # # Путь, где будет хранится результат
    # path = PATH+'/result.txt'
    # # Записываем результат
    # with open(path, 'w', encoding='utf8') as w_f:
    #     for key, value in data.items():z
    #         w_f.write(str(key) + " " + str(value) + "\n")

if __name__ == "__main__":
    '''
    start = time.time()
    parse_depth(WIKI_RANDOM, PATH)
    print(time.time() - start)
    '''
    start = time.time()
    merging_files()
    print(time.time() - start)
