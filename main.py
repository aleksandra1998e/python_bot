from my_bot.my_class import User
from my_bot.keyboards import yes_no_keyboard, start_keyboard, func_keyboard

import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging
import sqlite3
import datetime
from my_bot import start_help


logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

with sqlite3.connect('bd_bot.bd') as bd:
    cursor = bd.cursor()
    query = """ CREATE TABLE IF NOT EXISTS base_history(id INT, inquiry TEXT, information TEXT)"""
    cursor.execute(query)


@bot.message_handler(regexp='Привет')
@bot.message_handler(commands=['start', 'hello_world'])
def start_message(message):
    """Функция отвечающая на команды старт и привет мир
    И слово привет."""
    try:
        user = User.get_user(message.from_user.id)
        bot.send_message(message.chat.id, 'Привет!', reply_markup=start_keyboard)
        bot.send_message(message.chat.id, 'Ну что, начнем', reply_markup=func_keyboard)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


@bot.message_handler(commands=['help'])
def helper(message):
    """Функция отвечающая на команду помощь."""
    bot.send_message(
        message.chat.id, 'Что я умею:\n'
                         'Показать отели с самой низкой ценой (команда /lowprice)\n'
                         'Показать отели с самой высокой ценой (команда /highprice)\n'
                         'Показать отели в указанном ценовом диапазоне рядом с центром (команда /bestdeal)\n'
                         'Показать историю запросов (команда /history)\n\n'
                         'Также ты можешь воспользоваться кнопками на клавиатуре в любое удобное время.')


@bot.callback_query_handler(func=lambda call: call.data == 'lowprice')
def lowprice_seacher_handler(call: types):
    """Функция поиска самых дешевых отелей.
        через инлайн кнопку"""
    try:
        user = User.get_user(call.message.chat.id)
        user.search_data.append(list())
        user.search_data[-1].append('lowprice')
        msg = bot.send_message(call.message.chat.id, 'В каком городе будем искать?')
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(msg, city)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.message.chat.id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'highprice')
def highprice_seacher_handler(call: types):
    """Функция поиска самых дорогих отелей.
        через инлайн кнопку"""
    try:
        user = User.get_user(call.message.chat.id)
        user.search_data.append(list())
        user.search_data[-1].append('highprice')
        msg = bot.send_message(call.message.chat.id, 'В каком городе будем искать?')
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(msg, city)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.message.chat.id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'bestdeal')
def bestdeal_seacher_handler(call: types):
    """Функция поиска отелей в заданном ценовом
     диапазоне и расстоянии от центра.
        через инлайн кнопку"""
    try:
        user = User.get_user(call.message.chat.id)
        user.search_data.append(list())
        user.search_data[-1].append('bestdeal')
        msg = bot.send_message(call.message.chat.id, 'В каком городе будем искать?')
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(msg, price_range)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.message.chat.id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'history')
def history_seacher_handler(call: types):
    """Функция вывода истории поиска
         через инлайн кнопку"""
    try:
        pass
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.message.chat.id, 'Произошла ошибка...')


@bot.message_handler(commands=['lowprice'])
def lowprice_seacher_commands(message):
    """Функция поиска самых дешевых отелей.
    Через команду"""
    try:
        user = User.get_user(message.from_user.id)
        user.search_data.append(list())
        user.search_data[-1].append('lowprice')
        msg = bot.send_message(
            message.chat.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, city)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


@bot.message_handler(commands=['highprice'])
def highprice_seacher_commands(message):
    """Функция поиска самых самых дорогих отелей.
                Через команду"""
    try:
        user = User.get_user(message.from_user.id)
        user.search_data.append(list())
        user.search_data[-1].append('highprice')
        msg = bot.send_message(
            message.chat.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, city)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')

@bot.message_handler(commands=['bestdeal'])
def bestdeal_seacher_commands(message):
    """Функция поиска отелей в заданном ценовом
        диапазоне и расстоянии от центра.
                Через команду"""
    try:
        user = User.get_user(message.from_user.id)
        user.search_data.append(list())
        user.search_data[-1].append('bestdeal')
        msg = bot.send_message(
            message.chat.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, price_range)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


@bot.message_handler(commands=['history'])
def history_seacher_commands(message):
    """Функция вывода истории поиска.
            Через команду"""
    try:
        pass
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


def city(message):
    """Функция добавляет в список критериев поиска
    город и спрашивает количество отелей."""
    try:
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(message.text.lower())
        msg = bot.send_message(
            message.chat.id, 'Сколько отелей показать?\n   (не более 10 штук)')
        bot.register_next_step_handler(msg, hotels_count)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def hotels_count(message):
    """Функция добавляет в список критериев поиска
        количество отелей и спрашивает о том,
                нужны ли фотографии."""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id,
                                   'Количество должно быть числом, введите ещё раз.')
            bot.register_next_step_handler(msg, hotels_count)
            return
        elif int(message.text) > 10:
            msg = bot.send_message(message.chat.id,
                                   'Количество не более 10 штук, введите ещё раз.')
            bot.register_next_step_handler(msg, hotels_count)
            return
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(int(message.text))
        bot.send_message(
            message.chat.id, 'Желаете добавить фотографии отелей?', reply_markup=yes_no_keyboard)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def count_photo_yes(call):
    """Функция спрашивает количество фото."""
    try:
        msg = bot.send_message(call.message.chat.id,
                               'Введите количество фотографий.' 
                               '      (максимум 5)')
        bot.register_next_step_handler(msg, send_photo)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.inline_message_id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def count_photo_no(call):
    """Функция передает в качестве количества
    фотографии 0. И начинает поиск предложений"""
    try:
        user = User.get_user(call.message.chat.id)
        user.search_data[-1].append(0)
        msg = bot.send_message(call.message.chat.id,
                               'Начинаю поиск.')
        bot.register_next_step_handler(msg, search_any)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(call.inline_message_id, 'Произошла ошибка...')


def send_photo(message):
    """Функция добавляет в список критериев поиска
        количество фото. И начинает поиск предложений"""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id,
                                   'Количество должно быть числом, введите ещё раз.')
            bot.register_next_step_handler(msg, send_photo)
            return
        elif int(message.text) > 5:
            msg = bot.send_message(message.chat.id,
                                   'Количество не более 5 штук, введите ещё раз.')
            bot.register_next_step_handler(msg, send_photo)
            return
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(int(message.text))
        msg = bot.send_message(message.chat.id,
                               'Начинаю поиск.')
        bot.register_next_step_handler(msg, search_any)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


def price_range(message):
    """Функция добавляет в список критериев поиска город
        и спрашивает ценовой диапазон поиска."""
    try:
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(message.text)
        msg = bot.send_message(
            message.chat.id, 'Введите желаемую стоимость за сутки.\n(максимум и минимум через пробел)')
        bot.register_next_step_handler(msg, distance_range)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def distance_range(message):
    """Функция добавляет в список критериев поиска
            ценовой диапазон и спрашивает
        диапазон отдаленности от центра города."""
    try:
        price = message.text.split()
        print(price)
        if len(price) != 2 or not all([x.isdigit() for x in price]):
            msg = bot.send_message(message.chat.id,
                                   'Не правильный формат.\n'
                                   'Диапазон цен в формате "минимум" "максимум"')
            bot.register_next_step_handler(msg, distance_range)
            return
        print(price, message.text)
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(message.text)
        msg = bot.send_message(
            message.chat.id, 'Введите желаемое расстояние до центра.\n(максимум)')
        bot.register_next_step_handler(msg, hotels_count_bd)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def hotels_count_bd(message):
    """Функция добавляет в список критериев поиска
        диапазон отдаленности от центра города
        и спрашивает количество отелей."""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id,
                                   'Ошибка ввода.\n'
                                   'Расстояние должно быть целым числом.')
            bot.register_next_step_handler(msg, hotels_count_bd)
            return
        user = User.get_user(message.from_user.id)
        user.search_data[-1].append(message.text)
        msg = bot.send_message(
            message.chat.id, 'Сколько отелей показать?\n   (не более 10 штук)')
        bot.register_next_step_handler(msg, hotels_count)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')

def search_any():
    """В зависимости от первого аргумента в search_data
    буду вызывать тот или иной поиск"""
    pass


if __name__ == '__main__':
    bot.infinity_polling()
