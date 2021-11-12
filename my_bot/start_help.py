import telebot
from telebot import types
from dotenv import load_dotenv
import os
from my_bot.my_class import User

load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

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
