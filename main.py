from my_bot.my_class import User, MyTranslationCalendar
from my_bot.keyboards import yes_no_keyboard, start_keyboard, func_keyboard, currency_keyboard
from my_bot.check import check_city
from my_bot.price_sorter import price_sorter

import re
import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging
import datetime
#import sqlite3

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

# with sqlite3.connect('bd_bot.bd') as bd:
#     cursor = bd.cursor()
#     query = """ CREATE TABLE IF NOT EXISTS base_history(id INT, inquiry TEXT, information TEXT)"""
#     cursor.execute(query)


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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'lowprice'
        msg = bot.edit_message_text('В каком городе будем искать?',
                                    call.message.chat.id, call.message.message_id)
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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'highprice'
        msg = bot.edit_message_text('В каком городе будем искать?',
                                    call.message.chat.id, call.message.message_id)
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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'bestdeal'
        msg = bot.edit_message_text('В каком городе будем искать?',
                                    call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(call.id)
        bot.register_next_step_handler(msg, city)
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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'lowprice'
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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'highprice'
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
        user.search_data.append(dict())
        user.search_data[-1]['function'] = 'bestdeal'
        msg = bot.send_message(
            message.chat.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, city)
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
    """Функция уточняет город и проверяет его действительность"""
    try:
        user = User.get_user(message.from_user.id)
        if not check_city(message.text.lower(), bot, message.chat.id):
            msg = bot.send_message(message.chat.id,
                                   'Не могу понять, что это за город. Попробуйте ввести еще раз.')
            bot.register_next_step_handler(msg, city)
            return
    except Exception as e:
        print(f"bot happened in def city: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def city_id(call):
    """Функция добавляет в список критериев поиска
       город и спрашивает количество отелей или
       ценовой диапазон поиска в зависимости от запроса."""
    try:
        user = User.get_user(call.message.chat.id)
        user.search_data[-1]['city_id'] = str(call.data)
        bot.edit_message_text('Город выбран!',
                              call.message.chat.id, call.message.message_id,)
        bot.send_message(call.message.chat.id, 'Выберите валюту:',
                         reply_markup=currency_keyboard)
    except Exception as e:
        print(f"bot happened in def city_id: {e}")
        bot.send_message(User.users[call.message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data.startswith('currency'))
def currency_choice(call):
    """Функция добавляет в список критериев
                поиска валюту."""
    try:
        currency = call.data.split()
        user = User.get_user(call.message.chat.id)
        user.search_data[-1]['currency'] = currency[1]
        bot.edit_message_text(f'Выбрана валюта {currency[1]}',
                              call.message.chat.id, call.message.message_id)
        hotels_count(call.message)
    except Exception as e:
        print(f"bot happened in def currency_choice: {e}")
        bot.send_message(User.users[call.message.chat.id].id, 'Произошла ошибка...')


def hotels_count(message):
    try:
        """Функция спрашивает количество отелей или
        ценовой диапазон поиска в зависимости от запроса."""
        user = User.get_user(message.chat.id)
        if not user.search_data[-1]['function'] == 'bestdeal':
            msg = bot.send_message(
                message.chat.id, 'Сколько отелей показать?\n   (не более 10 штук)')
            bot.register_next_step_handler(msg, photo)
        else:
            msg = bot.send_message(
                message.chat.id,
                'Введите желаемую стоимость за сутки.\n(максимум и минимум через пробел)')
            bot.register_next_step_handler(msg, price_range)
    except Exception as e:
        print(f"bot happened in def hotels_count: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def photo(message):
    """Функция добавляет в список критериев поиска
        количество отелей и спрашивает о том,
                нужны ли фотографии."""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id,
                                   'Количество должно быть числом, введите ещё раз.')
            bot.register_next_step_handler(msg, photo)
            return
        elif int(message.text) > 10:
            msg = bot.send_message(message.chat.id,
                                   'Количество не более 10 штук, введите ещё раз.')
            bot.register_next_step_handler(msg, photo)
            return
        user = User.get_user(message.from_user.id)
        user.search_data[-1]['hotels_count'] = message.text
        bot.send_message(
            message.chat.id, 'Желаете добавить фотографии отелей?', reply_markup=yes_no_keyboard)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def count_photo_yes(call):
    """Функция спрашивает количество фото."""
    try:
        msg = bot.edit_message_text('Введите количество фотографий. (максимум 5)',
                                    call.message.chat.id, call.message.message_id)
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
        user.search_data[-1]['photo_count'] = str(0)
        bot.edit_message_text('Какие даты смотрим?',
                              call.message.chat.id, call.message.message_id)
        calendar_build_checkin(call.message.chat.id)
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
        user.search_data[-1]['photo_count'] = message.text
        bot.send_message(message.chat.id,
                         'Какие даты смотрим?')
        calendar_build_checkin(message.chat.id)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


def price_range(message):
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
            bot.register_next_step_handler(msg, price_range)
            return
        print(price, message.text)
        user = User.get_user(message.from_user.id)
        user.search_data[-1]['range_price'] = message.text
        msg = bot.send_message(
            message.chat.id, 'Введите максимальное расстояние до центра в километрах.\n'
                             '(Примеры: 2 3.6 12,2)')
        bot.register_next_step_handler(msg, distance_range)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def distance_range(message):
    """Функция добавляет в список критериев поиска
        диапазон отдаленности от центра города
        и спрашивает количество отелей."""
    try:
        if not re.fullmatch(r'\d+[.,]?\d+', message.text):
            msg = bot.send_message(message.chat.id,
                                   'Ошибка ввода.\n'
                                   'Расстояние должно числом.\n'
                                   'Допускается использование точки или запятой.')
            bot.register_next_step_handler(msg, distance_range)
            return
        user = User.get_user(message.from_user.id)
        user.search_data[-1]['range_distance'] = message.text
        msg = bot.send_message(
            message.chat.id, 'Сколько отелей показать?\n   (не более 10 штук)')
        bot.register_next_step_handler(msg, hotels_count)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def search_any(id):
    """В зависимости от первого аргумента в search_data
    буду вызывать тот или иной поиск"""
    try:
        user = User.get_user(id)
        if (user.search_data[-1]['function'] == 'lowprice') or (user.search_data[-1]['function'] == 'highprice'):
            price_sorter(user)
            for hotels in user.answer:
                bot.send_message(id, 'Отель {hotel}\n'
                                     'Адрес: {address}\n'
                                     'До центра города {distance} км.\n'
                                     'Цена за сутки: {price}\n'
                                     'Бронь на выбранные даты: {total_price} {cur}.'.format(
                    hotel=hotels["name"], address=hotels["address"],
                    distance=hotels["distance"], price=hotels["price"],
                    total_price=hotels["total_price"], cur=user.search_data[-1]['currency']
                ))
                for ph_url in hotels["photo_url"]:
                    bot.send_photo(id, photo=ph_url.format(size='z'))
    except Exception as e:
        print(f"bot happened in def search_any: {e}")
        bot.send_message(User.users[id].id, 'Произошла ошибка...')


def calendar_build_checkin(message):
    """Построение календаря начиная с сегодняшней даты"""
    try:
        calendar, step = MyTranslationCalendar(calendar_id=1, locale='ru', min_date=datetime.date.today()).build()
        bot.send_message(message,
                         f"Выберите дату заезда:",
                         reply_markup=calendar)
    except Exception as e:
        print(f"bot happened in def calendar_build_checkin: {e}")
        bot.send_message(User.users[message].id, 'Произошла ошибка...')


def calendar_build_checkout(message):
    """Построение календаря начиная с выбранной даты заезда"""
    try:
        user = User.get_user(message)
        calendar, step = MyTranslationCalendar(calendar_id=2, locale='ru',
                                               min_date=user.search_data[-1]['date check inn']).build()
        bot.send_message(message,
                         f"Выберите дату выезда:",
                         reply_markup=calendar)
    except Exception as e:
        print(f"bot happened in def calendar_build_checkout: {e}")
        bot.send_message(User.users[message].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=MyTranslationCalendar.func(calendar_id=1))
def cal_checkin(call):
    """Выбор даты заезда в отель"""
    try:
        result, key, step = MyTranslationCalendar(calendar_id=1, locale='ru', min_date=datetime.date.today()
                                                  ).process(call.data)
        if not result and key:
            bot.edit_message_text(f"Выберите дату заезда:",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Заезд {result}",
                                  call.message.chat.id,
                                  call.message.message_id)
            user = User.get_user(call.message.chat.id)
            user.search_data[-1]['date check inn'] = result
            calendar_build_checkout(call.message.chat.id)
    except Exception as e:
        print(f"bot happened in def cal_checkin: {e}")
        bot.send_message(User.users[call.message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=MyTranslationCalendar.func(calendar_id=2))
def cal_checkout(call):
    """Выбор даты выезда из отеля"""
    try:
        user = User.get_user(call.message.chat.id)
        result, key, step = MyTranslationCalendar(calendar_id=2, locale='ru',
                                                  min_date=user.search_data[-1]['date check inn']
                                                  ).process(call.data)
        if not result and key:
            bot.edit_message_text(f"Выберите дату выезда:",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Выезд {result}",
                                  call.message.chat.id,
                                  call.message.message_id)
            user = User.get_user(call.message.chat.id)
            user.search_data[-1]['date check out'] = result
            bot.send_message(
                call.message.chat.id, 'Приступаю к поиску!')
            search_any(call.message.chat.id)
    except Exception as e:
        print(f"bot happened in def cal_checkout: {e}")
        bot.send_message(User.users[call.message.chat.id].id, 'Произошла ошибка...')


if __name__ == '__main__':
    bot.infinity_polling()
