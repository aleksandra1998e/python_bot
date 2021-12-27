import requests
import json
from telebot import types
import re
import os


def new_city_keyboards(response):
    """Создает варианты написного в сообщении города
            и выводит их в виде кнопок"""

    city_keyboards = types.InlineKeyboardMarkup(row_width=1)
    for i in response["suggestions"]:
        if i["group"] == "CITY_GROUP":
            for j in i["entities"]:
                city_name = re.sub(r'<.+?>', '', j["caption"])
                city_keyboards.add(
                    types.InlineKeyboardButton(city_name, callback_data=
                        j["destinationId"]
                ))
    return city_keyboards


def check_city(city, bot, id):
    '''Проверяет cуществует ли предложенный город'''

    rapidapi_key = os.environ.get('rapidapi_key')
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring_first = {"query": city, "locale": "ru_RU", "currency": "RUB"}
    querystring_second = {"query": city, "locale": "en_EN", "currency": "USD"}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }

    response = requests.request("GET", url, headers=headers, params=querystring_first)
    response_json = json.loads(response.text)
    if response_json["moresuggestions"] != 0:
        keyboard = new_city_keyboards(response_json)
        bot.send_message(
            id, 'Выберите подходящий вариант:',
            reply_markup=keyboard)
        return True
    else:
        response = requests.request("GET", url, headers=headers, params=querystring_second)
        response_json = json.loads(response.text)
        if response_json["moresuggestions"] != 0:
            keyboard = new_city_keyboards(response_json)
            bot.send_message(
                id, 'Выберите подходящий вариант:',
                reply_markup=keyboard)
            return True
    return False
