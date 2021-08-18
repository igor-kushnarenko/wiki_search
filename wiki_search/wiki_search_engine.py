import os

import wikipedia

import json


class DataBase:
    def __init__(self, db_name):
        self.db = db_name
        if not self.db:
            self.create_new_db()

    def create_new_db(self):
        data = {}
        with open(self.db, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_db(self):
        with open(self.db, 'r') as f:
            data = json.load(f)
        return data

    def write_db(self, page, data, response):
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
        with open(self.db, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return data[response]


class WikiSearchEngine:
    def __init__(self, response, data):
        self.response = response
        self.data = data

    def search_to_db(self):
        for key, value in self.data.items():
            if self.response == key:
                return value

    def search_to_web(self):
        self.response = self.response.lower().capitalize()
        try:
            page = wikipedia.page(self.response)
            search = wikipedia.search(self.response)
        except wikipedia.exceptions.DisambiguationError as ex:
            page = wikipedia.page(ex.args[1][0])
            search = wikipedia.search(ex.args[1][0])
        except wikipedia.exceptions.PageError as ex:
            page = wikipedia.page(ex.args[0])
            search = wikipedia.search(ex.args[0])
        return page, search


class Menu:
    def main_menu(self):
        response = input('Введите запрос: ')
        db = DataBase('wiki_data.json')
        data = db.read_db()
        search = WikiSearchEngine(response, data)
        res = search.search_to_db()
        if res:
            return res
        else:
            page = search.search_to_web()
            result = db.write_db(page[0], data, response)
            search = page[1]  # TODO добавить возможные варианты
            return result


if __name__ == '__main__':
    wikipedia.set_lang('ru')

    while True:
        result = Menu().main_menu()
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