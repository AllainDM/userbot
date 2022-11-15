import config
from aiogram import Bot, Dispatcher, executor, types
import os
import parser
import time
from datetime import datetime

# bot_answer = False  # Получили ли мы ответ в последний раз

# bot = Bot(token=config.BOT_API_TOKEN, parse_mode=types.ParseMode.HTML)
bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start5'])
async def self_message(message):
    try:
        # global bot_answer
        await bot.send_message(message.chat.id, f"Ответ: Бот запущен")
        while True:
            time.sleep(30)
            mes = parser.bot_start()
            try:
                if len(mes) > 0:
                    # await bot.send_message(message.chat.id, f"Ответ: {mes}")
                    x = 0
                    for i in mes:
                        await bot.send_message(message.chat.id, f"Ответ: {mes[x]}")
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
                await bot.send_message(message.chat.id, f"Ответ: Ошибка с получением ответа от парсера")
                # bot_answer = True
                # print(f"{datetime.now()}: bot_answer = True")
            # finally:
            #     pass
    except:
        print(f"{datetime.now()}: Ошибка с таймером")
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Ошибка с таймером \n")
        file.close()
        await bot.send_message(message.chat.id, f"Ответ: Ошибка с таймером")


def working():
    file = open("logs.txt", "a")
    file.write(f"{datetime.now()}: Программа запущена \n")
    file.close()
    while True:
        time.sleep(1800)
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Программа работает \n")
        file.close()


if __name__ == '__main__':
    executor.start_polling(dp)
    working()
