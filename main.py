from datetime import datetime
import requests
import os
import logging
import time

from aiogram import Bot, Dispatcher, executor, types

import parser
import config

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w")
logging.debug("A DEBUG Message")
logging.info("An INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message of CRITICAL severity")

# bot_answer = False  # Получили ли мы ответ в последний раз

# bot = Bot(token=config.BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


# @dp.message_handler(commands=['start6'])
# async def self_message(message):
#     try:
#         # global bot_answer
#         await bot.send_message(message.chat.id, f"Ответ: Бот запущен")
#         while True:
#             time.sleep(30)
#             mes = parser.bot_start()
#             try:
#                 if len(mes) > 0:
#                     # await bot.send_message(message.chat.id, f"Ответ: {mes}")
#                     x = 0
#                     for i in mes:
#                         await bot.send_message(message.chat.id, f"Ответ: {mes[x]}")
#                         x += 1
#                 else:
#                     print(f"{datetime.now()}: Новых ремонтов нет")
#                     file = open("logs.txt", "a")
#                     file.write(f"{datetime.now()}: Новых ремонтов нет \n")
#                     file.close()
#             except:
#                 print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
#                 file = open("logs.txt", "a")
#                 file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
#                 file.close()
#                 await bot.send_message(message.chat.id, f"Ответ: Ошибка с получением ответа от парсера")
#                 # bot_answer = True
#                 # print(f"{datetime.now()}: bot_answer = True")
#             # finally:
#             #     pass
#     except:
#         print(f"{datetime.now()}: Ошибка с таймером")
#         file = open("logs.txt", "a")
#         file.write(f"{datetime.now()}: Ошибка с таймером \n")
#         file.close()
#         await bot.send_message(message.chat.id, f"Ответ: Ошибка с таймером")


def working():
    pass
    # file = open("logs.txt", "a")
    # file.write(f"{datetime.now()}: Программа запущена \n")
    # file.close()
    # while True:
    #     time.sleep(1800)
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Программа работает \n")
    #     file.close()


def start_parsing():
    mes = parser.bot_start()
    try:
        if len(mes) > 0:
            # await bot.send_message(message.chat.id, f"Ответ: {mes}")
            x = 0
            for i in mes:
                # await bot.send_message(message.chat.id, f"Ответ: {mes[x]}")
                send_telegram(mes[x])
                x += 1
        else:
            print(f"{datetime.now()}: Новых ремонтов нет")
            file = open("logs.txt", "a")
            file.write(f"{datetime.now()}: Новых ремонтов нет \n")
            file.close()
    except:
        print(f"{datetime.now()}: Ошибка с получением ответа от парсера")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Ошибка с получением ответа от парсера \n")
        file.close()
        # await bot.send_message(message.chat.id, f"Ответ: Ошибка с получением ответа от парсера")
        send_telegram(f"Ответ: Ошибка с получением ответа от парсера")
    # bot_answer = True
    # print(f"{datetime.now()}: bot_answer = True")
    # finally:
    #     pass


def send_telegram(text):
    # text = format_text(offer)
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data = {
        'chat_id': config.chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url=url, data=data)


def format_text():
    pass


def main():
    send_telegram("Бот запущен")
    # start_parsing()
    # try:
        # start_parsing()
        # !!!!! Отключу цикл для тестов
    while True:
        time.sleep(180)
        start_parsing()
    # except e as n:
    #     send_telegram("Ошибка с таймером")
    #     print(f"{datetime.now()}: Ошибка с таймером")
    #     file = open("logs.txt", "a")
    #     file.write(f"{datetime.now()}: Ошибка с таймером \n")
    #     file.close()


if __name__ == '__main__':
    # executor.start_polling(dp)
    # working()
    main()
