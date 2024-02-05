import json
import time
import sched
import requests
import telebot
import os
from telebot.types import InputMediaPhoto
from back import keep_alive

BOT_TOKEN = os.environ['BOT_TOKEN']
URL = os.environ['URL']
s = sched.scheduler(time.time, time.sleep)
token = BOT_TOKEN
bot = telebot.TeleBot(token)
keep_alive()
def get_messages():
    try:
        response = requests.post(URL)
        response.raise_for_status()  # Бросает исключение, если статус ответа - ошибка
    except Exception as e:
        bot.send_message(-4157560547, f'сообщение не сгенерировалось: {str(e)}')
        return None

    try:
        data = response.json()
    except ValueError:
        bot.send_message(-4157560547, f'Ошибка при разборе ответа как JSON')
        return None

    if not isinstance(data, list) or len(data) != 4:
        bot.send_message(-4157560547, f'Ответ не в ожидаемом формате')
        return None

    return data


def send_message(sc):

    message = get_messages()
    try:
        bot.send_photo(chat_id = -4157560547, photo = str(message[1]), caption = f'Сообщение: {str(message[0])} \n mood: {str(message[2])} \n Роль: {str(message[3])}')
    except Exception as e:
        bot.send_message(-4157560547, f'Приколямба для анализа:{message} \n Ошибка: {str(e)}')
    s.enter(600,1, send_message, (sc,))
s.enter(600, 1 , send_message, (s,))
s.run()

