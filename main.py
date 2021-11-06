import logging
from telegram import InlineKeyboardButton, Bot, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler,  ConversationHandler,  CallbackContext
import os
from dotenv import load_dotenv

LOWPRICE, HIGHTPRICE, BESTDEAL, HISTORY = range(4)
keyboard_static = [[KeyboardButton("/help")],
                   [KeyboardButton("/lowprice")],
                   [KeyboardButton("/hightprice")],
                   [KeyboardButton("/bestdeal")],
                   [KeyboardButton("/history")]]

keyboard_first = [[InlineKeyboardButton("Самые дешевые отели", callback_data='LOWPRICE')],
                  [InlineKeyboardButton("Самые дорогие отели", callback_data='HIGHTPRICE')],
                  [InlineKeyboardButton("Отели близко к центру", callback_data='BESTDEAL')],
                  [InlineKeyboardButton("История запросов", callback_data='HISTORY')]]

keyboard_count = [[InlineKeyboardButton("5", callback_data=5),
                  InlineKeyboardButton("10", callback_data=10)],
                  [InlineKeyboardButton("15", callback_data=15),
                  InlineKeyboardButton("20", callback_data=20)]]


def start(update, _):
    update.message.reply_text('Привет', reply_markup=ReplyKeyboardMarkup(keyboard_static))
    reply_markup = InlineKeyboardMarkup(keyboard_first, one_time_keyboard=True)
    update.message.reply_text('Что будем смотреть?', reply_markup=reply_markup)


def hello_world(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет")
    reply_markup = InlineKeyboardMarkup(keyboard_first)
    update.message.reply_text('Что будем смотреть?', reply_markup=reply_markup)


def text_hi(update, context):
    if update.message.text == 'Привет':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='И тебе привет')
        reply_markup = InlineKeyboardMarkup(keyboard_first)
        update.message.reply_text('Что будем смотреть?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Извини, я тебя не понимаю...\nНапиши лучше Привет')


def help_fun(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Что я умею:\nПоказать отели с самой низкой ценой (команда /lowprice)\n'
                                  'Показать отели с самой высокой ценой (команда /highprice)\n'
                                  'Показать отели в указанном ценовом диапазоне рядом с центром (команда /bestdeal)\n'
                                  'Показать историю запросов (команда /history)\n\n'
                                  'Также ты можешь воспользоваться кнопками на клавиатуре в любое удобное время.'
                             )
    reply_markup = InlineKeyboardMarkup(keyboard_first)
    update.message.reply_text('Что будем смотреть?', reply_markup=reply_markup)

def lowprice(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Тут будет функция поиска дешевых отелей')

def hightprice(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Тут будет функция поиска дорогих отелей')

def bestdeal(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Тут будет функция поиска отелей близко к центру')

def history(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Тут будет функция вывода истории запросов')


load_dotenv()
TOKEN = os.environ.get('TOKEN')
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


dispatcher.add_handler(CallbackQueryHandler(lowprice, pattern='LOWPRICE'))
dispatcher.add_handler(CallbackQueryHandler(hightprice, pattern='HIGHTPRICE'))
dispatcher.add_handler(CallbackQueryHandler(bestdeal, pattern='BESTDEAL'))
dispatcher.add_handler(CallbackQueryHandler(history, pattern='HISTORY'))
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('hello_world', hello_world))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_hi))
dispatcher.add_handler(CommandHandler('help', help_fun))
dispatcher.add_handler(CommandHandler('lowprice', lowprice))
dispatcher.add_handler(CommandHandler('hightprice', hightprice))
dispatcher.add_handler(CommandHandler('bestdeal', bestdeal))
dispatcher.add_handler(CommandHandler('history', history))


if __name__ == '__main__':
    updater.start_polling()

