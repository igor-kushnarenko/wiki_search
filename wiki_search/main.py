import json
import os

import wikipedia

wikipedia.set_lang('ru')

print('ДОБРО ПОЖАЛОВАТЬ В ПОИСК ПО ВИКИПЕДИИ!')
print()

if not os.path.exists('wiki_data.json'):
    with open('wiki_data.json', 'w') as file:
        json.dump({}, file)


def search_in_data(response, data):
    """Функция ищет запрос в json файле"""
    for key, value in data.items():
        if response == key:
            return value


def search_wiki(response, data):
    """Функция ищет запрос на сайте wikipedia"""
    response = response.lower().capitalize()
    page = wikipedia.page(response)
    title = page.title
    summary = page.summary
    content = page.content
    url = page.url
    data[response] = {
        'title': title,
        'summary': summary,
        'url': url,
        'content': content,
    }
    with open('wiki_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return data[response]


def run():
    """Поиск запроса сначала по базе, потом на сайте."""
    usr = input('Введите запрос: ')
    with open('wiki_data.json', 'r') as file:
        data = json.load(file)
        res = search_in_data(usr, data)
        if res:
            return res
        else:
            info = search_wiki(usr, data)
            return info


if __name__ == '__main__':
    while True:
        result = run()
        print(f'{result["summary"]}\n{result["url"]}')
        print('1.Подробнее')
        print('2.Новый поиск')
        print('3.Выход')
        user_input = int(input('Ввод: '))
        if user_input == 1:
            print(result['content'])
        elif user_input == 2:
            continue
        elif user_input == 3:
            break