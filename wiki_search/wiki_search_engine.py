import os

import wikipedia

import json


class DataBase:
    """Класс содержащий методы для работы с Базой Данных"""
    def __init__(self, db_name):
        self.db = db_name
        if not self.db:
            self.create_new_db()

    def create_new_db(self):
        """Создание новой БД"""
        data = {}
        with open(self.db, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def read_db(self):
        """Чтение БД"""
        with open(self.db, 'r') as f:
            data = json.load(f)
        return data

    def write_db(self, page_list, data, response):
        """Запись в БД спарсенных данных из wikipedia"""
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
    """Поиск по БД и в wikipedia"""
    def __init__(self, response, data):
        self.response = response
        self.data = data

    def search_to_db(self):
        """Поиск в БД по ключевому слову"""
        for key, value in self.data.items():
            if self.response == key:
                return value

    def search_to_web(self):
        """Поиск в wikipedia с обработкой исключений связанных с опечатками при вводе"""
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
    """Класс принимающий ключевое слово и выводящий меню для пользователя"""
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
            return result

    def main_menu(self, response):
        wikipedia.set_lang('ru')
        while True:
            result = self.take_result(response)
            print(f'\n{result["summary"]}\n{result["url"]}')
            print('\n1.ПОДБРОБНЕЕ\n2.НОВЫЙ ПОИСК\n3.ВЫХОД')
            chooses = [f'{index+1}. {x}' for index, x in enumerate(result['choose'], 3)]
            print(f'! ВАМ МОЖЕТ БЫТЬ ИНТЕРЕСНО: {", ".join(chooses)}')
            user_input = int(input('Ввод: '))
            if user_input == 1:
                print(f"\n{result['content']}")
            elif user_input == 2:
                self.run()
            elif user_input == 3:
                break
            elif user_input == 4:
                TerminalMenu().main_menu(chooses[0])
            elif user_input == 5:
                TerminalMenu().main_menu(chooses[1])
            elif user_input == 6:
                TerminalMenu().main_menu(chooses[2])
            elif user_input == 7:
                TerminalMenu().main_menu(chooses[3])
            elif user_input == 8:
                TerminalMenu().main_menu(chooses[4])
            elif user_input == 9:
                TerminalMenu().main_menu(chooses[5])
            elif user_input == 10:
                TerminalMenu().main_menu(chooses[6])
            elif user_input == 11:
                TerminalMenu().main_menu(chooses[7])
            elif user_input == 12:
                TerminalMenu().main_menu(chooses[8])
            elif user_input == 13:
                TerminalMenu().main_menu(chooses[9])

    def run(self):
        response = input('Введите запрос: ')
        TerminalMenu().main_menu(response)


if __name__ == '__main__':
    TerminalMenu().run()
    # DataBase('wiki_data.json').create_new_db()