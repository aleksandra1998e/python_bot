from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, MessageHandler,  Filters, ConversationHandler, CallbackContext
import logging

logger = logging.getLogger(__name__)
keyboard_count = [[InlineKeyboardButton("5", callback_data=5),
                  InlineKeyboardButton("10", callback_data=10)],
                  [InlineKeyboardButton("15", callback_data=15),
                  InlineKeyboardButton("20", callback_data=20)]]
keyboard_answer = [[InlineKeyboardButton("Да", callback_data='YES')],
                  [InlineKeyboardButton("Нет", callback_data='NO')]]
keyboard_count_photo = [[InlineKeyboardButton("1", callback_data=1),
                  InlineKeyboardButton("3", callback_data=3)],
                  [InlineKeyboardButton("5", callback_data=5),
                  InlineKeyboardButton("10", callback_data=10)]]



CITY, COUNT, PHOTO, ANSWER = range(3)


def lowprice(update, _):
    update.message.reply_text('Введи город, где ищем отели.')
    return CITY


def search_city(update, _):
    city = update.message.from_user
    logger.info("Пользователь {} ищет город {}".format(city.first_name, update.message.text))
    print(logger.info)
    update.message.reply_text(
        text='Количество отелей, которые нужно вывести:',
        reply_markup=InlineKeyboardMarkup(keyboard_count)
    )
    return COUNT


def count(update, _):
    #user = update.message.from_user
    query = update.callback_query
    hotels_count = query.data
    query.answer()
    logger.info("Количество запрошенных отелей = {}".format(
        str(hotels_count)
    ))
    print(logger.info)
    update.message.reply_text(
        text='Добавить фотографии?',
        reply_markup=InlineKeyboardMarkup(keyboard_answer)
    )
    return PHOTO

def photo(update, context):
    update.message.reply_text(
        text='Количество отелей, которые нужно вывести:',
        reply_markup=InlineKeyboardMarkup(keyboard_count)
    )


def skip_photo(update, context):
    pass

def cancel(update, context):
    return ConversationHandler.END


lowprice_handler = ConversationHandler(
    entry_points=[CommandHandler('lowprice', lowprice)],
    states={CITY: [MessageHandler(Filters.text & (~Filters.command), search_city)],
            COUNT: [CallbackQueryHandler(count)],
            PHOTO: [CallbackQueryHandler(photo, pattern='YES'),
                    CallbackQueryHandler(skip_photo, pattern='NO')]

            },
    fallbacks=[CommandHandler('cancel', cancel)]
)
dispatcher.add_handler(lowprice_handler)
