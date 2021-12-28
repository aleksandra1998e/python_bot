import requests
import json
import re
import os


def photo_url(user, count):
    rapidapi_key = os.environ.get('rapidapi_key')
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": user.answer[-1]["id"]}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    photos = requests.request("GET", url, headers=headers, params=querystring)
    a_json = json.loads(photos.text)

    i = 0
    while i < count:
        for j in a_json["roomImages"]:
            for ph in j["images"]:
                if i < count:
                    user.answer[-1]["photo_url"].append(ph["baseUrl"])
                    i += 1
        else:
            break
    while i < count:
        for j in a_json["hotelImages"]:
            if i < count:
                user.answer[-1]["photo_url"].append(j["baseUrl"])
                i += 1
        else:
            break


def hot_search(user, hotel):
    user.answer.append(dict())
    user.answer[-1]["id"] = hotel["id"]
    user.answer[-1]["name"] = hotel.get("name", 'не найдено')
    user.answer[-1]["urls"] = 'https://www.hotels.com/ho' + str(hotel["id"])
    user.answer[-1]["address"] = hotel["address"].get("streetAddress", 'не найдено')
    distance = float(hotel["landmarks"][0]["distance"].split()[0]) * 1.609
    user.answer[-1]["distance"] = round(distance, 2)
    user.answer[-1]["price"] = hotel["ratePlan"]["price"].get("current", 'не найдено')
    total_price_1 = (hotel["ratePlan"]["price"].get("fullyBundledPricePerStay", 'не найдено'))
    if total_price_1 == 'не найдено':
        total_price = user.answer[-1]["price"].split()
        if re.search(r',', total_price[0]):
            total_price[0] = re.sub(r',', '.', total_price[0])
        days = (user.search_data[-1]['date check out'] - user.search_data[-1]['date check inn']).days
        user.answer[-1]["total_price"] = float(total_price[0]) * days
    else:
        user.answer[-1]["total_price"] = (total_price_1.split())[1]
    user.answer[-1]["photo_url"] = list()
    photo_url(user, int(user.search_data[-1]['photo_count']))


def price_sorter(user):
    rapidapi_key = os.environ.get('rapidapi_key')
    url = "https://hotels4.p.rapidapi.com/properties/list"
    if user.search_data[-1]['function'] == 'lowprice':
        parameter = "PRICE"
    else:
        parameter = "PRICE_HIGHEST_FIRST"
    querystring = {"destinationId": user.search_data[-1]['city_id'], "pageNumber": "1",
                   "pageSize": user.search_data[-1]['hotels_count'],
                   "checkIn": user.search_data[-1]['date check inn'],
                   "checkOut": user.search_data[-1]['date check out'],

                   "adults1": "1", "sortOrder": parameter,
                   "currency": user.search_data[-1]['currency'],
                   }
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    a_json = json.loads(response.text)
    hotel_list = a_json["data"]["body"]["searchResults"]["results"]
    user.answer.clear()

    for hotel in hotel_list:
        hot_search(user, hotel)


