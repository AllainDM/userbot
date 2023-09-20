from datetime import datetime
import requests
import os
import time

from aiogram import Bot, Dispatcher, executor, types

import parser
import config

# bot = Bot(token=config.BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


# Функция эхо бота для проверки работоспособности и получения ид чата
@dp.message_handler(commands=['0'])
async def echo_mess(message: types.Message):
    await bot.send_message(message.chat.id, "Бот работает")
    # await bot.send_message(message.chat.id, message.chat.id)
    print(message.chat.id)
    print("Сообщение отправлено")


def start_parsing():
    mes = parser.bot_start()
    # Ответ приходит в виде списка списков, под каждый район
    # 0 индекс Адмирал
    # try:
    if len(mes[0]) > 0:
        for i in mes[0]:
            send_telegram_old_admiral(i)
    else:
        print(f"{datetime.now()}: Новых ремонтов нет")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Новых ремонтов нет \n")
        file.close()
    # except:
    #     print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
    #     file.close()
    #     send_telegram_old_admiral(f"Ответ: Ошибка с получением ответа от парсера")

    # 1 индекс Центр
    # try:
    if len(mes[1]) > 0:
        for i in mes[1]:
            send_telegram_centre(i)
    else:
        print(f"{datetime.now()}: Новых ремонтов нет")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Новых ремонтов нет \n")
        file.close()
    # except:
    #     print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
    #     file.close()
    #     send_telegram_centre(f"Ответ: Ошибка с получением ответа от парсера")

    # 2 индекс Адмирал новый
    # try:
    if len(mes[2]) > 0:
        for i in mes[2]:
            # send_telegram_new_admiral(i)
            send_telegram_new_admiral(i)
    else:
        print(f"{datetime.now()}: Новых ремонтов нет")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Новых ремонтов нет \n")
        file.close()
    # except:
    #     print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
    #     file.close()
    #     send_telegram_new_admiral(f"Ответ: Ошибка с получением ответа от парсера")

    # 3 Подключить быстрее
    # try:
    if len(mes[3]) > 0:
        for i in mes[3]:
            # send_telegram_fast(i)
            send_telegram_fast(i)
    else:
        print(f"{datetime.now()}: Новых ремонтов нет")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Новых ремонтов нет \n")
        file.close()
    # except:
    #     print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
    #     file.close()
    #     send_telegram_fast(f"Ответ: Ошибка с получением ответа от парсера")


def send_telegram_new_admiral(text_to_bot):
    # text = format_text(offer)
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data_to_chat = {
        'chat_id': config.chat_id_new_admiral,
        'text': text_to_bot,
        'parse_mode': 'HTML'
    }
    requests.post(url=url, data=data_to_chat)

    # Доп сообщение в личку юзеру отключено. На тесте телеграмм банил из-за большого количества запросов
    if config.send_to_telegram_user:
        data_to_user = {
            'chat_id': config.user_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url, data=data_to_user)


def send_telegram_old_admiral(text_to_bot):
    # text = format_text(offer)
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data_to_chat = {
        'chat_id': config.chat_id_old_admiral,
        'text': text_to_bot,
        'parse_mode': 'HTML'
    }
    requests.post(url=url, data=data_to_chat)

    # Доп сообщение в личку юзеру отключено. На тесте телеграмм банил из-за большого количества запросов
    if config.send_to_telegram_user:
        data_to_user = {
            'chat_id': config.user_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url, data=data_to_user)


def send_telegram_fast(text_to_bot):
    # text = format_text(offer)
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data_to_chat = {
        'chat_id': config.chat_id_for_fast,
        'text': text_to_bot,
        'parse_mode': 'HTML'
    }
    requests.post(url=url, data=data_to_chat)

    # Доп сообщение в личку юзеру отключено. На тесте телеграмм банил из-за большого количества запросов
    if config.send_to_telegram_user:
        data_to_user = {
            'chat_id': config.user_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url, data=data_to_user)


def send_telegram_centre(text_to_bot):
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data_to_chat = {
        'chat_id': config.chat_id_for_centre,
        'text': text_to_bot,
        'parse_mode': 'HTML'
    }
    requests.post(url=url, data=data_to_chat)

    # Доп сообщение в личку юзеру отключено. На тесте телеграмм банил из-за большого количества запросов
    if config.send_to_telegram_user:
        data_to_user = {
            'chat_id': config.user_id,
            'text': text_to_bot,
            'parse_mode': 'HTML'
        }
        requests.post(url=url, data=data_to_user)


def format_text():
    pass


def main():
    # send_telegram_new_admiral("Бот запущен")
    # send_telegram_old_admiral("Бот запущен")
    # send_telegram_fast("Бот запущен")
    # send_telegram_centre("Бот запущен")
    start_parsing()
    while True:
        time.sleep(config.delay)
        start_parsing()


if __name__ == '__main__':
    # executor.start_polling(dp)  # Вариант для эхо-бота, для тестов
    main()
