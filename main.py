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
    try:
        if len(mes) > 0:
            # await bot.send_message(message.chat.id, f"Ответ: {mes}")
            x = 0
            for i in mes:
                # await bot.send_message(message.chat.id, f"Ответ: {mes[x]}")
                # TODO тут наверное надо не mes[x], а просто i
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
        send_telegram(f"Ответ: Ошибка с получением ответа от парсера")


def send_telegram(text_to_bot):
    # text = format_text(offer)
    url = f'https://api.telegram.org/bot{config.BOT_API_TOKEN}/sendMessage'
    data_to_chat = {
        'chat_id': config.chat_id,
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
    send_telegram("Бот запущен")
    start_parsing()
    while True:
        time.sleep(config.delay)
        start_parsing()


if __name__ == '__main__':
    # executor.start_polling(dp) # Вариант для эхо-бота, для тестов
    main()
