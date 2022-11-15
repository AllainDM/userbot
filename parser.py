import requests
import config
import time
from bs4 import BeautifulSoup
from datetime import datetime
# from main import bot_answer

session = requests.Session()

url_login = "http://us.gblnet.net/oper/"
url_filter = "http://us.gblnet.net/oper/?core_section=task_list&filter_selector0=task_state&task_state0_value=1&filter_" \
       "selector1=task_staff&employee_find_input=&employee_id1=877"
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
        soup = BeautifulSoup(html.text, 'lxml')
        new_list_repairs_id = []  # Сюда запишем список всех найденных ремонтов, список будет считаться как новый
        table = soup.find_all('tr', class_="cursor_pointer")
        a = 0  # Счетчик количества заявок, для теста
        # Ищем все ссылки в которых в описании номер ремонта
        # Создаем список номеров ремонтов
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
            x = 0  # Счетчик индексов новых ремонтов, предполагается, что все новые ремонты появляются вверху,
            # но бывают ремонты, появляются где-нибудь посередине
            for i_new in new_list_repairs_id:
                if list_repairs_id.count(i_new) == 0:
                    # print(f"""Ремонт: {i_new} не найден в списке""")
                    # Отдельный список только новых ремонтов, нужен только для лога
                    new_repair_id.append(i_new)
                    # list_index.append(x)  # Добавляем индекс ремонта в новом списке, что не правильно
                    answer.append(table[x].text)
                    answer.append(f"{url_link_repair}{i_new}")
                    # answer.append(x)
                x += 1
            answer.reverse()
            h = " ".join(new_list_repairs_id)
            # h = string.join(iterable)
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
    else:
        print("error")


def bot_start():
    return get_html(url_filter)
