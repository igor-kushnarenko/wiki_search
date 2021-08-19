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

    def write_db(self, page_list, data, response):
        page = page_list[0]
        choose = page_list[1]
        title = page.title
        summary = page.summary
        content = page.content
        url = page.url
        data[response] = {
            'title': title,
            'summary': summary,
            'url': url,
            'content': content,
            'choose': choose,
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


class TerminalMenu:
    def take_result(self, response):
        db = DataBase('wiki_data.json')
        data = db.read_db()
        search = WikiSearchEngine(response, data)
        res = search.search_to_db()
        if res:
            return res
        else:
            page = search.search_to_web()
            result = db.write_db(page, data, response)
            search = page[1]  # TODO добавить возможные варианты
            return result

    def main_menu(self):
        wikipedia.set_lang('ru')
        while True:
            response = input('Введите запрос: ')
            result = self.take_result(response)
            print(f'{result["summary"]}\n{result["url"]}')
            print('1.ПОДБРОБНЕЕ\n2.НОВЫЙ ПОИСК\n3.ВЫХОД')
            chooses = [f'{index+1}. {x}' for index, x in enumerate(result['choose'], 3)]
            print(f'! ВАМ МОЖЕТ БЫТЬ ИНТЕРЕСНО: {", ".join(chooses)}')

            user_input = int(input('Ввод: '))
            if user_input == 1:
                print(result['content'])
            elif user_input == 2:
                continue
            elif user_input == 3:
                break
            elif user_input == 4:
                self.take_result(chooses[0])


if __name__ == '__main__':
    TerminalMenu().main_menu()
    # DataBase('wiki_data.json').create_new_db()