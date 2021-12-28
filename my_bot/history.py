import sqlite3
import datetime


def sql(user) -> None:
    '''Функция добавляет в базу данных запрос от пользователя'''

    with sqlite3.connect('bot.bd') as bd:
        cursor = bd.cursor()
        query = """ CREATE TABLE IF NOT EXISTS users_history(
        user INT,  date TEXT, time INT, func TEXT, hotels TEXT)"""
        cursor.execute(query)
        hotels = []
        for h in user.answer:
            hotels.append(h["name"])

        mydate = int(user.id), str(user.search_data[-1]['date']), int(
            (user.search_data[-1]['date'] - datetime.datetime(2020, 1, 1)).total_seconds()
        ), str(user.search_data[-1]['function']), str(hotels)
        cursor.execute("""INSERT INTO users_history VALUES(?, ?, ?, ?, ?)""", mydate)


def history_user(user, my_seconds: int) -> list:
    try:
        with sqlite3.connect('bot.bd') as bd:
            cursor = bd.cursor()
            my_time = (datetime.datetime.now() - datetime.datetime(2020, 1, 1)).total_seconds() - my_seconds
            user_id = user.id, my_time
            query = """SELECT date, func, hotels FROM users_history WHERE user = ? and time >=  ?
            ORDER BY time"""
            cursor.execute(query, user_id)
            answer = cursor.fetchall()
            return answer
    except Exception:
        return None


