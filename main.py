import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging
import datetime
import sqlite3
from my_bot.my_class import User
import sqlite3
from my_bot import start_help


logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s: %(name)s - %(levelname)s - %(message)s')
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
user_dict = {}

with sqlite3.connect('bd_bot.bd') as bd:
    cursor = bd.cursor()
    query = """ CREATE TABLE IF NOT EXISTS base_history(id INT, inquiry TEXT, information TEXT)"""
    cursor.execute(query)

yes_no_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1, btn2 = types.InlineKeyboardButton("Да", callback_data='yes'),\
             types.InlineKeyboardButton("Нет", callback_data='no')
yes_no_keyboard.add(btn1, btn2)

start_keyboard = types.ReplyKeyboardMarkup(row_width=1)
btn1, btn2, btn3, btn4, btn5 = types.KeyboardButton('/lowprice'), types.KeyboardButton('/highprice'),\
                                types.KeyboardButton('/bestdeal'), types.KeyboardButton('/history'), \
                                types.KeyboardButton('/help')
start_keyboard.add(btn1, btn2, btn3, btn4, btn5)

func_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1, btn2, btn3, btn4 = types.InlineKeyboardButton("Самые дешевые", callback_data='lowprice'), \
                               types.InlineKeyboardButton("Самые дорогие", callback_data='highprice'),\
                               types.InlineKeyboardButton("Близко к центру", callback_data='bestdeal'), \
                               types.InlineKeyboardButton("История запросов", callback_data='history')
func_keyboard.add(btn1, btn2, btn3, btn4)


@bot.message_handler(regexp='Привет')
@bot.message_handler(commands=['start', 'hello_world'])
def start_message(message):
    """Функция отвечающая на команды старт и привет мир
    И слово привет."""
    if message.chat.id not in User.users.keys():
        user = User(message.chat.id)
    try:
        user = User.users[message.chat.id].id
        bot.send_message(user, 'Привет!', reply_markup=start_keyboard)
        bot.send_message(user, 'Ну что, начнем', reply_markup=func_keyboard)
    except:
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


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
def lowprice_seacher_handler(call):
    """Функция поиска самых дешевых отелей.
        через инлайн кнопку"""
    try:
        if call.inline_message_id not in User.users.keys():
            user = User(call.inline_message_id)
        else:
            user = User.users[call.inline_message_id]
        user.search_data.clear()
        user.search_data.append('lowprice')
        msg = bot.send_message(call.inline_message_id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, city)
    except:
        bot.send_message(call.inline_message_id, 'Произошла ошибка...')


@bot.message_handler(commands=['lowprice'])
def lowprice_seacher_commands(message):
    """Функция поиска самых дешевых отелей.
    Через команду"""
    try:
        if message.chat.id not in User.users.keys():
            user = User(message.chat.id)
        else:
            user = User.users[message.chat.id]
        user.search_data.clear()
        user.search_data.append('lowprice')
        msg = bot.send_message(
            message.chat.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, city)
    except:
        bot.send_message(message.chat.id, 'Произошла ошибка...')


def city(message):
    """Функция добавляет в список критериев поиска
    город."""
    try:
        user = User.users[message.chat.id]
        user.search_data.append(message.text.lower())
        msg = bot.send_message(
            message.chat.id, 'Сколько отелей показать?\n  (не более 10 штук)')
        bot.register_next_step_handler(msg, hotels_count)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


def hotels_count(message):
    """Функция добавляет в список критериев поиска
    количество отелей."""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat_id,
                                   'Количество должно быть числом, введите ещё раз.')
            bot.register_next_step_handler(msg, hotels_count)
        elif int(message.text) > 10:
            msg = bot.send_message(message.chat_id,
                                   'Количество не более 10 штук, введите ещё раз.')
            bot.register_next_step_handler(msg, hotels_count)
        user = User.users[message.chat.id]
        user.search_data.append(int(message.text))
        bot.send_message(
            message.chat.id, 'Желаете добавить фотографии отелей?', reply_markup=yes_no_keyboard)
    except:
        bot.send_message(User.users[message.chat.id].id, 'Произошла ошибка...')


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def count_photo(call):
    """Функция спрашивает количество фото."""
    try:
        msg = bot.send_message(call.inline_message_id,
                               'Введите количество фотографий.' 
                               '      (максимум 5)')
        bot.register_next_step_handler(msg, send_photo)
    except:
        bot.send_message(call.inline_message_id, 'Произошла ошибка...в каунте')


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def count_photo(call):
    """Функция передает в качестве количества
    фотографии 0."""
    try:
        print(call.inline_message_id)
        user = User.users[call.inline_message_id]
        user.search_data.append(0)
        msg = bot.send_message(call.inline_message_id,
                               'Начинаю поиск.')
        bot.register_next_step_handler(msg, search_any)
    except:
        bot.send_message(call.inline_message_id, 'Произошла ошибка...')


def send_photo(message):
    """Функция добавляет в список критериев поиска
        количество фото."""
    try:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat_id,
                                   'Количество должно быть числом, введите ещё раз.')
            bot.register_next_step_handler(msg, send_photo)
        elif int(message.text) > 5:
            msg = bot.send_message(message.chat_id,
                                   'Количество не более 5 штук, введите ещё раз.')
            bot.register_next_step_handler(msg, send_photo)
        user = User.users[message.chat.id]
        user.search_data.append(int(message.text))
        msg = bot.send_message(message.chat_id,
                               'Начинаю поиск.')
        bot.register_next_step_handler(msg, search_any)
    except Exception as e:
        print(f"bot happened: {e}")
        bot.send_message(message.chat.id, 'Произошла ошибка...')


def search_any():
    """В зависимости от первого аргумента в search_data
    буду вызывать тот или иной поиск"""
    pass




if __name__ == '__main__':
    bot.infinity_polling()

