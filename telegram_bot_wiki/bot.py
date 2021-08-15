# -*- coding: utf-8 -*-
import time

import telebot
from telebot import types

from wiki_search_engine import run

bot = telebot.TeleBot(token='1411367870:AAESw3tboLtob_Lf_en8WBVbea3y7ldbH94')
USER_ID = set()


# @bot.callback_query_handler(func=lambda message: True)
# def callback_inlines(message):
#     if 'answer' in message.data:
#         first_word = run(message.text)
#         answer = first_word['content']
#         bot.send_message(
#             message.chat.id,
#             answer,
#             reply_markup=answer_keyboard(message.chat.id),
#         )


@bot.message_handler(commands=['start'])
def send_welcome(message):
    answer = f'Привет! С моей помощью, ты сможешь найти на Википедии интересующую тебя информацию!'
    bot.send_message(
        message.chat.id,
        answer,
    )


@bot.callback_query_handler(func=lambda message: True)
def send_content(message):
    if 'answer' in message.data:
        first_word = run(message.text)
        answer = first_word['content']
        print(answer)
        bot.send_message(
            message.chat.id,
            answer,
            reply_markup=answer_keyboard(message.chat.id),
        ) # TODO 'CallbackQuery' object has no attribute 'text'


# анализатор текста :)
@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text:
        first_word = run(message.text)
        answer = (first_word['summary'], first_word['url'])
        answer = '\n'.join(answer)
        bot.send_message(
            message.chat.id,
            answer,
            reply_markup=answer_keyboard(message.chat.id),
        )

    # elif message.text == 'Подробнее...':
    #     bot.send_message(
    #         message.chat.id,
    #         'Это подробность.',
    #         reply_markup=main_keyboard,
    #     )


# функция для инлайн клавиатуры которая появляется при выборе Аудио: "elif message.text == 'Практика (аудио)...':"
def answer_keyboard(chat_id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Подробнее...',
        callback_data='answer'),
    )
    return keyboard


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            time.sleep(3)
            print(ex)