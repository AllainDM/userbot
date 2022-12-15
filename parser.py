import requests
from datetime import datetime

from bs4 import BeautifulSoup

import config
import main
# from main import bot_answer

session = requests.Session()

url_login = "http://us.gblnet.net/oper/"
url_with_filter = "http://us.gblnet.net/oper/?core_section=task_list&filter_selector0=task_state&task_state0_value=" \
                  "1&filter_selector1=task_staff&employee_find_input=&employee_id1=877"
url_link_repair = "http://us.gblnet.net/oper/?core_section=task&action=show&id="

HEADERS = {
    "main": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0"
}

data = {
    "action": "login",
    "username": config.loginUS,
    "password": config.pswUS
}
response = session.post(url_login, data=data, headers=HEADERS).text

# list_repairs_id = []
# new_repair_id = []  # Список новых ремонтов, делаем глобально, чтоб при необходимости отправлять повторно
# old_answer = []  # Тот самый ответ боту, который мы можем отправить повторно

with open("list.txt", "r") as f:
    text = f.read()
    new_text = text.split(" ")
    # global list_repairs_id
    list_repairs_id = new_text
    print(f"{datetime.now()}: Читаем из файла: {text}")
    print(f"{datetime.now()}: Читаем из файла: {new_text}")


def get_html(url):
    html = session.get(url)
    global list_repairs_id
    new_repair_id = []  # Список ид новых ремонтов
    # global old_answer # Сохраним ответ глобально, для возможности повторной отправки
    answer = []  # Ответ боту
    if html.status_code == 200:
        # try:
        soup = BeautifulSoup(html.text, 'lxml')
        new_list_repairs_id = []  # Сюда запишем список всех найденных ремонтов, список будет считаться как новый
        table = soup.find_all('tr', class_="cursor_pointer")
        # print(table[0])
        a = 0  # Счетчик количества заявок, для теста
        # Ищем все ссылки в которых в описании номер ремонта
        # Создаём список номеров ремонтов
        for i in table:  # Цикл по списку всей таблицы
            list_a = i.find_all('a')  # Ищем ссылки во всей таблице
            for ii in list_a:  # Цикл по найденным ссылкам
                if len(ii.text) == 6:  # Ищем похожесть на ид ремонта, он всегда из 6 цифр(еще на несколько лет)
                    # В список новых ремонтов добавляется номер ремонта
                    new_list_repairs_id.append(ii.text)
                    a += 1  # Счетчик количества заявок, для теста
        print(f"{datetime.now()}: Всего ремонтов: {a}")  # Счетчик количества заявок, для теста
        # print(f"{datetime.now()}: Ошибка с таймером")
        # Запись лога
        file = open("logs.txt", "a")
        file.write(f"{datetime.now()}: Всего ремонтов: {a} \n")
        file.close()
        # Самая простая проверка совпадения списка, если вообще ничего не изменилось
        # list_index = []  # Список индексов отсутствующих ремонтов
        if new_list_repairs_id == list_repairs_id:
            print(f"{datetime.now()}: Списки совпадают")
            # Запись лога
            file = open("logs.txt", "a")
            file.write(f"{datetime.now()}: Списки совпадают \n")
            file.close()
            # Если списки не совпали, то через цикл ищем новые ремонты
        else:
            # answer = make_answer(table, new_list_repairs_id)
            x = 0  # Счетчик индексов новых ремонтов, предполагается, что все новые ремонты появляются вверху,
            # но бывают ремонты, появляются где-нибудь посередине
            for i_new in new_list_repairs_id:
                if list_repairs_id.count(i_new) == 0:
                    # print(f"""Ремонт: {i_new} не найден в списке""")
                    new_repair_id.append(i_new)  # Отдельный список только новых ремонтов, нужен только для лога
                    # Далее нужно составить текст ответа для бота
                    repair_link = url_link_repair + i_new  # Ссылка будет в конце
                    td_class_all = table[x].find_all('td', class_="")
                    print(td_class_all)
                    td_class_div_center_all = table[x].find_all('td', class_="div_center")
                    data_repair = td_class_div_center_all[1]
                    # print(f"""data_repair_all: {data_repair}""")
                    # print(f"""data_repair: {data_repair}""")

                    address_repair = td_class_all[0]
                    address_repair_text = address_repair.text
                    # print(f"""address_repair: {address_repair.text}""")
                    # print(f"""address_repair: {address_repair}""")

                    mission_repair = td_class_all[1].b
                    # print(f"""mission_repair: {mission_repair.text}""")

                    comment_repair = table[x].find_all('div', class_="div_journal_opis")
                    print(comment_repair)

                    # Комментария может не быть, поэтому делаем проверку
                    if len(comment_repair) > 0:
                        # print(f"""comment_repair: {comment_repair}""")
                        # print(f"""comment_repair: {comment_repair[0]}""")
                        # print(f"""comment_repair: {comment_repair[0].text}""")
                        comment_repair = comment_repair[0].text
                    else:  # Если коммента нет создаем пустую строку
                        comment_repair = " "

                    one_repair_text = f"{mission_repair.text} \n\n {address_repair_text} \n\n " \
                                      f"{data_repair.text} \n\n {comment_repair} \n\n {repair_link}"
                    answer.append(one_repair_text)
                x += 1
            answer.reverse()
            # Обновим список ремонтов в файлике, для его прочтения при перезапуске бота
            # !!!!!! Отключу запись временно для теста скорости. На скорость не влияет
            # Так же отключаю для теста редактирования вывода текста бота, чтоб выводить всегда старые ремонты
            h = " ".join(new_list_repairs_id)
            file = open("list.txt", "w")
            file.write(h)
            file.close()

        # Обновляем глобально список ид ремонтов
        list_repairs_id = new_list_repairs_id
        # Список новых ремонтов, по факту нужен только для лога
        if len(new_repair_id) > 0:
            # print(f"{datetime.now()}: Список индексов: {list_index}")
            print(f"{datetime.now()}: Список новых ремонтов: {new_repair_id}")
            file = open("logs.txt", "a")
            file.write(f"{datetime.now()}: Список новых ремонтов: {new_repair_id} \n")
            file.close()
        return answer
        # except IndexError as e:
        #     main.send_telegram(f"""Ошибка с парсером: {e}""")
        #     print(f"{datetime.now()}: Ошибка с парсером: {e}")
        #     file = open("logs.txt", "a")
        #     file.write(f"{datetime.now()}: Ошибка с парсером: {e} \n")
        #     file.close()
    else:
        print("error")


def make_answer(table, new_list_repairs_id):
    answer = []

    return answer


def bot_start():
    return get_html(url_with_filter)
