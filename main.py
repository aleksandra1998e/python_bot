import logging
from telegram import InlineKeyboardButton, Bot, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackQueryHandler

keyboard = [[InlineKeyboardButton("тест", callback_data='1')],
            [InlineKeyboardButton("тест", callback_data='2')],
            [InlineKeyboardButton("тест", callback_data='3')]
    ]


def button(update, _):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Что-то будет происходить")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет")
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Что-то буду спрашивать:', reply_markup=reply_markup)


def hello_world(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привет")
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Что-то буду спрашивать:', reply_markup=reply_markup)


def text_hi(update, context):
    if update.message.text == 'Привет':
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='И тебе привет')
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Что-то буду спрашивать:', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Извини, я тебя не понимаю...\nНапиши лучше Привет')


TOKEN = '2105160266:AAE6u1jMMp8aecPQnqWMiyyC-F_vHmR4Jzo'
bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# обработчик команды старт
start_handler = CommandHandler('start' or 'hello_world', start)
dispatcher.add_handler(start_handler)

# обработчик команды hello_world
hello_word_handler = CommandHandler('hello_world', hello_world)
dispatcher.add_handler(hello_word_handler)

# обработчик текстовых сообщений
text_hi_handler = MessageHandler(Filters.text & (~Filters.command), text_hi)
dispatcher.add_handler(text_hi_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))

if __name__ == '__main__':
    updater.start_polling()

