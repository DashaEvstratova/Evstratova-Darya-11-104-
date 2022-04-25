"""get values from wiki site with bs4"""

import requests
from bs4 import BeautifulSoup
from validators import url as valid_url

WIKI_RANDOM = 'https://ru.wikipedia.org/wiki/Special:Random'
WIKI_DOMAIN = "https://ru.wikipedia.org"
PATH = r'C:/Users/dasha/PycharmProjects/Evstratova-Darya-11-104'


def get_byte(url):
    """mothod to get byte_code"""
    # Извлекаем данные из ссылки
    response = requests.get(url)
    # Переводим содержимое ссылки в байт код
    code = response.content
    return code


def soup_of_code(code):
    """method get html cod"""
    # Достаем html код
    soup = BeautifulSoup(code, 'lxml')
    return soup


def get_urls(soup):
    """get all url"""
    # Поиск по атрибуту и отсеивание лишнего
    new_soup = soup.select('div[class=mw-parser-output]')
    # Проверка на то, что после новый список не пустой
    if len(new_soup) == 0:
        return []
    # Выбираем из списка ссылки
    urls = new_soup[0].findAll('a')
    # Создаем список для вики ссылок
    link_wiki = []
    for elem in urls:
        # Достаем ссылку без тэгов
        link = str(elem.get("href"))
        # Поверка что сссылка на страницу вики
        if '/wiki/' in link:
            url = WIKI_DOMAIN + link
            # Если ссылка рабочая, то дабавляем в список ссылок
            if valid_url(url):
                link_wiki.append(url)
    return link_wiki

def put_text(soup, data_cls):
    """put words and count them"""
    # Создается объект класса
    data = data_cls()
    # Достаем текст со страниц вики с тэгами
    text = soup.find('div', class_="mw-parser-output")
    # Проверяем, что на странице есть текст
    if text is None:
        return data
    # Содержимое текста
    text = text.text
    # Преобразовываем текст в список слов
    words = list(map(lambda s: s.lower().strip(), filter(lambda s: s.isalpha(), text.split())))
    # Проходимся по всем словам
    for elem in words:
        # Проверяем на наличие слова в мапе
        if elem in data:
            # Если есть, то счетчик увеличиваем
            data[elem] = data[elem] + 1
        else:
            # В противгном случае добавляем со значением один
            data[elem] = 1
    return data

if __name__ == "__main__":
    print(get_urls(soup_of_code(get_byte(WIKI_RANDOM))))
