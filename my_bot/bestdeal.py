import re
import json
import requests
from .price_sorter import hot_search, photo_url
import os


def besdeal_req(user):
    rapidapi_key = os.environ.get('rapidapi_key')
    parameter = "DISTANCE_FROM_LANDMARK"
    price_range = user.search_data[-1]['range_price'].split()
    price_min = min(price_range)
    price_max = max(price_range)
    user.search_data[-1]['range_distance'] = re.sub(r',', '.', user.search_data[-1]['range_distance'])
    mil = round(float(user.search_data[-1]['range_distance']) * 0.62, 1)

    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': rapidapi_key
    }
    querystring = {"destinationId": user.search_data[-1]['city_id'], "pageNumber": "1",
                   "pageSize": user.search_data[-1]['hotels_count'],
                   "checkIn": user.search_data[-1]['date check inn'],
                   "checkOut": user.search_data[-1]['date check out'],
                   "priceMin": price_min, "priceMax": price_max,
                   "adults1": "1", "sortOrder": parameter,
                   "currency": user.search_data[-1]['currency'],
                   "landmarkIds": str(mil)
                   }

    response = requests.request("GET", url, headers=headers, params=querystring)
    a_json = json.loads(response.text)
    hotel_list = a_json["data"]["body"]["searchResults"]["results"]
    user.answer.clear()
    for hotel in hotel_list:
        hot_search(user, hotel)
