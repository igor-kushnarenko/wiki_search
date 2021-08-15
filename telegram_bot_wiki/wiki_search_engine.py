import json
import os

import wikipedia

wikipedia.set_lang('ru')

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
    page = wikipedia.page(response)
    summary = page.summary
    content = page.content
    url = page.url
    data[response] = {
        'summary': summary,
        'url': url,
        'content': content,
    }
    with open('wiki_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    return data[response]


def run(question):
    """Поиск запроса сначала по базе, потом на сайте."""
    with open('wiki_data.json', 'r') as file:
        data = json.load(file)
        res = search_in_data(question, data)
        if res:
            return res
        else:
            info = search_wiki(question, data)
            return info


# if __name__ == '__main__':
    # result = run('Анапа')
    # print(result)