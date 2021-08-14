import json

import wikipedia

wikipedia.set_lang('ru')


def search_in_data(response, data):
    for key, value in data.items():
        if response == key:
            return value


def search_wiki(response):
    with open('wiki_data.json', 'r') as file:
        data = json.load(file)
        res = search_in_data(usr, data)
        if res:
            return res
        else:
            page = wikipedia.page(response)
            summary = page.summary
            content = page.content
            url = page.url
            info = {response: {
                'summary': summary,
                'url': url,
                'content': content,
            }}
            with open('wiki_data.json', 'w') as file:
                json.dump(info, file, ensure_ascii=False, indent=4)
            return info


if __name__ == '__main__':
    while True:
        usr = input('Введите запрос: ')
        result = search_wiki(usr)
        print(f'{result}\n{result["url"]}')
        print('1.Подробнее\n2.Новый поиск\n3.Выход')
        user_input = int(input('Ввод: '))
        if user_input == 1:
            print(result['content'])
        elif user_input == 2:
            continue
        elif user_input == 3:
            break



