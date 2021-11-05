import logging
from telegram import InlineKeyboardButton, Bot, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler

keyboard_static = [[KeyboardButton("/help")],
                   [KeyboardButton("/lowprice")],
                   [KeyboardButton("/highprice")],
                   [KeyboardButton("/bestdeal")],
                   [KeyboardButton("/history")]
    ]
keyboard_first = [[InlineKeyboardButton("Самые дешевые", callback_data='lowprice')],
                  [InlineKeyboardButton("Самые дорогие", callback_data='highprice')],
                  [InlineKeyboardButton("Близко к центру", callback_data='bestdeal')],
                  [InlineKeyboardButton("История запросов", callback_data='history')]
    ]


def button(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Что-то будет происходить")


def start(update, _):
    update.message.reply_text('Привет', reply_markup=ReplyKeyboardMarkup(keyboard_static))
    reply_markup = InlineKeyboardMarkup(keyboard_first)
    update.message.reply_text('Начнем', reply_markup=reply_markup)


def hello_world(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет")
    reply_markup = InlineKeyboardMarkup(keyboard_first)
    update.message.reply_text('Что-то буду спрашивать:', reply_markup=reply_markup)


def text_hi(update, context):
    if update.message.text == 'Привет':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='И тебе привет')
        reply_markup = InlineKeyboardMarkup(keyboard_first)
        update.message.reply_text('Что-то буду спрашивать:', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Извини, я тебя не понимаю...\nНапиши лучше Привет')


def help_fun(update, context):
    pass

def lowprice(update, context):
    pass

def hightprice(update, context):
    pass

def bestdeal(update, context):
    pass

def history(update, context):
    pass


TOKEN = '2105160266:AAE6u1jMMp8aecPQnqWMiyyC-F_vHmR4Jzo'
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# обработчик кнопок
dispatcher.add_handler(CallbackQueryHandler(button))

# обработчик команды старт
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# обработчик команды hello_world
hello_word_handler = CommandHandler('hello_world', hello_world)
dispatcher.add_handler(hello_word_handler)

# обработчик текстовых сообщений
text_hi_handler = MessageHandler(Filters.text & (~Filters.command), text_hi)
dispatcher.add_handler(text_hi_handler)

# обработчик команды help
help_handler = CommandHandler('help', help_fun)
dispatcher.add_handler(help_handler)

# обработчик команды lowprice
lowprice_handler = CommandHandler('lowprice', help_fun)
dispatcher.add_handler(lowprice_handler)

# обработчик команды hightprice
hightprice_handler = CommandHandler('hightprice', help_fun)
dispatcher.add_handler(hightprice_handler)

# обработчик команды bestdeal
bestdeal_handler = CommandHandler('bestdeal', help_fun)
dispatcher.add_handler(bestdeal_handler)

# обработчик команды history
history_handler = CommandHandler('history', help_fun)
dispatcher.add_handler(history_handler)


if __name__ == '__main__':
    updater.start_polling()

