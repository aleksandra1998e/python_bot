from telebot import types

yes_no_keyboard = types.InlineKeyboardMarkup(row_width=1, )
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

currency_keyboard = types.InlineKeyboardMarkup(row_width=1)
btn1, btn2, btn3 = types.InlineKeyboardButton("Рубль", callback_data='currency RUB'), \
                        types.InlineKeyboardButton("Доллар", callback_data='currency USD'),\
                        types.InlineKeyboardButton("Евро", callback_data='currency EUR')
currency_keyboard.add(btn1, btn2, btn3)