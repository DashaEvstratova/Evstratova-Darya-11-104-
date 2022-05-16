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
        # Создать байт код
        byte_code = get_byte(url)
        # Открыть файл для записиси байт кода
        with open(''.join([page_path, '/content.xml']), 'wb') as file:
            # Записываем байт код
            file.write(byte_code)
    else:
        # В противном случае, открываем уже готовый файл с байт кодом
        with open(''.join([page_path, '/content.xml']), 'rb') as file:
            # Достаем байт код
            byte_code = file.read()

    # Достаем содержимое по байт коду
    soup = soup_of_code(byte_code)
    # Обрабатывает слова через мапу
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
            # Добавляются ссылки и удаляютсся дубликаты
            urls = set(next_step) - urls

def get_file(filename):
    '''iteration'''
    # Открываем файл для чтения
    with open(filename, 'r',  encoding='utf8') as inp:
        # Считываем строку
        line = inp.readline()
        # Проходимся по всему файлу
        while len(line)>1:
            # Вытаскиваем слово и количество
            key, value = line.split()
            # Делаем количесиво числом
            value = int(value)
            # Возвращается слово и количество
            yield key, value
            # Переходим к следующей строке
            line = inp.readline()

def merge(iterator1, iterator2):
    '''merge two iteration'''
    # Массивс результатом, соединенные файлы
    result = []
    # Первые элементы двух итераторов, ели же нет элемента, то None
    ferst_iter = next(iterator1, None)
    second_iter = next(iterator2, None)
    # Пока оба генератора работают, сливать их
    while ferst_iter is not None and second_iter is not None:
        # Если ключ второго итератора раньше, то записываем его и переходим дальше
        if ferst_iter[0] > second_iter[0]:
            result.append(second_iter)
            second_iter = next(iterator2, None)
        # Если ключ первого итератора раньше, то записываем его и переходим дальше
        elif ferst_iter[0] < second_iter[0]:
            result.append(ferst_iter)
            ferst_iter = next(iterator1, None)
        # Если ключи равны, то складываем и переходим дальше
        else:
            result.append((ferst_iter[0], ferst_iter[1]+second_iter[1]))
            ferst_iter = next(iterator1, None)
            second_iter = next(iterator2, None)
    # В случае, если второй закончился, то досливаем первый
    while ferst_iter is not None:
        result.append(ferst_iter)
        ferst_iter = next(iterator1, None)
    # В случае, если первый закончился, то досливаем второй
    while second_iter is not None:
        result.append(second_iter)
        second_iter = next(iterator2, None)
    # Возвращаем итератор результата
    return iter(result)

def sorting(arr):
    '''sort iterators'''
    # Если всего один файл, то просто его возвращаем
    if len(arr) == 1:
        return arr[0]
    # Находим медиану
    middle = len(arr) //2
    # Рекурсивно разделяем массив итераторов, потом по два сливаем
    return merge(sorting(arr[:middle]), sorting(arr[middle:]))

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
    # Директория, где хранится файл с результатом
    res = ''.join([PATH, '/result.txt'])
    # Список всех слов и их количество
    resulting = sorting(data)
    # Открываем для записи
    with open(res, 'w', encoding='utf8') as writ:
        # Закидываем результат в файл
        for key, value in resulting:
            writ.write(str(key) + " " + str(value) + "\n")

if __name__ == "__main__":
    start = time.time()
    parse_depth(WIKI_RANDOM, PATH)
    print(time.time() - start)
    start = time.time()
    merging_files()
    print(time.time() - start)
