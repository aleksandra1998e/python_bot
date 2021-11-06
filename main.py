import telebot
from telebot import types
import os
from dotenv import load_dotenv
import logging
import datetime

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
user_dict = {}
search_data = []

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

yes_no_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1, btn2 = types.InlineKeyboardButton("Да", callback_data='yes'),\
             types.InlineKeyboardButton("Нет", callback_data='no')
yes_no_keyboard.add(btn1, btn2)


@bot.message_handler(regexp='Привет')
@bot.message_handler(commands=['start', 'hello_world'])
def start_message(message):
    """Функция отвечающая на команды старт и привет мир
    И слово привет."""
    bot.send_message(message.chat.id, 'Привет!', reply_markup=start_keyboard)
    bot.send_message(message.chat.id, 'Ну что, начнем', reply_markup=func_keyboard)
    try:
        chat_id = message.chat.id
        if chat_id not in user_dict.keys():
            user_dict[chat_id] = list()
        print(user_dict)
    except Exception:
        bot.reply_to(message, 'Произошла ошибка...')


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
@bot.message_handler(commands=['lowprice'])
def lowprice_seacher(message):
    """Функция поиска самых дешевых отелей."""
    msg = bot.send_message(
        message.chat.id, 'В каком городе будем искать?')  #'CallbackQuery' object has no attribute 'chat_id'
    search_data.clear()                                   # Если вызывать через инлайн кнопки
    search_data.append('lowprice')
    user_dict[message.chat.id].append("Функция поиска самых дешевых отелей.")
    user_dict[message.chat.id].append(str(datetime.datetime.now()))
    bot.register_next_step_handler(msg, city)


def city(message):
    """Функция добавляет в список критериев поиска
    город."""
    search_data.append(message.text.lower())
    msg = bot.send_message(
        message.chat.id, 'Сколько отелей показать?\n  (не более 15 штук)')
    bot.register_next_step_handler(msg, hotels_count)


def hotels_count(message):
    """Функция добавляет в список критериев поиска
    количество отелей."""
    if not message.text.isdigit():
        msg = bot.send_message(message.chat_id,
                               'Количество должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, hotels_count)
    elif int(message.text) > 15:
        msg = bot.send_message(message.chat_id,
                               'Количество не более 15 штук, введите ещё раз.')
        bot.register_next_step_handler(msg, hotels_count)
    search_data.append(int(message.text))
    bot.send_message(
        message.chat.id, 'Желаете добавить фотографии отелей?', reply_markup=yes_no_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def count_photo(message):
    """Функция спрашивает количество фото."""
    msg = bot.send_message(message.chat_id,                 #'CallbackQuery' object has no attribute 'chat_id'
                           'Введите количество фотографий.' #ТА ЖЕ ПРОБЛЕМА КАК НА 68. Инлайн кнопки
                           '      (максимум 5)')
    bot.register_next_step_handler(msg, send_photo)


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def count_photo(message):
    """Функция передает в качестве количества
    фотографии 0."""
    search_data.append(0)
    msg = bot.send_message(message.chat_id,
                           'Начинаю поиск.')
    bot.register_next_step_handler(msg, search_any)


def send_photo(message):
    """Функция добавляет в список критериев поиска
        количество фото."""
    if not message.text.isdigit():
        msg = bot.send_message(message.chat_id,
                               'Количество должно быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, send_photo)
    elif int(message.text) > 5:
        msg = bot.send_message(message.chat_id,
                               'Количество не более 5 штук, введите ещё раз.')
        bot.register_next_step_handler(msg, send_photo)
    search_data.append(int(message.text))
    msg = bot.send_message(message.chat_id,
                           'Начинаю поиск.')
    bot.register_next_step_handler(msg, search_any)


def search_any():
    """В зависимости от первого аргумента в search_data
    буду вызывать тот или иной поиск"""
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'highprice')
@bot.message_handler(commands=['highprice'])
def helper(message):
    """Функция поиска самых дорогих отелей."""
    bot.send_message(
        message.chat.id, 'Функция поиска самых дорогих отелей')


@bot.callback_query_handler(func=lambda call: call.data == 'bestdeal')
@bot.message_handler(commands=['bestdeal'])
def helper(message):
    """Функция поиска отелей в заданном
     ценовом диапазоне рядом с центром."""
    bot.send_message(
        message.chat.id, 'Функция поиска отелей в заданном '
                         'ценовом диапазоне рядом с центром.')


@bot.callback_query_handler(func=lambda call: call.data == 'history')
@bot.message_handler(commands=['history'])
def helper(message):
    """Вывод истории поиска."""
    bot.send_message(
        message.chat.id, 'Вывод истории поиска')


if __name__ == '__main__':
    bot.infinity_polling()

