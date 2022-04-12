from pyparsing import *
import datetime
import sqlite3
from sqlite3 import *
import PySimpleGUI as sg
import time

data = datetime.datetime.today() - datetime.timedelta(1)  # текущая дата и время


# SQL
def create_connection(path):  # Создание БД
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Подключение к SQLite БД успешно")
    except Error as e:
        print(f"Ошибка при подключении к SQLite БД: '{e}'")

    return connection


def execute_query(connection, query):  # Запрос к БД
    curs = connection.cursor()
    try:
        curs.execute(query)
        connection.commit()
        print("Запрос выполнен успешно")
    except Error as e:
        print(query)
        print(f"Ошибка при запросе: '{e}'")


# Таблица Parsing
create_table_pars = """ 
CREATE TABLE Parsing (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name_FULL VARCHAR NULL DEFAULT NULL,
  Type_mes VARCHAR NULL DEFAULT NULL,
  File_path VARCHAR NULL DEFAULT NULL,
  Line_num_file VARCHAR NULL DEFAULT NULL,
  Time_m VARCHAR NULL DEFAULT NULL,
  Cause VARCHAR NULL DEFAULT NULL,
  Prefix VARCHAR NULL DEFAULT NULL,
  Message VARCHAR NULL DEFAULT NULL,
  Num_str INTEGER NULL DEFAULT NULL,
  Comments VARCHAR NULL DEFAULT NULL,
  FOREIGN KEY (Type_mes) REFERENCES Quantity(Name));
"""
# Таблица Quantity
create_table_quant = """
CREATE TABLE Quantity (  
  Name VARCHAR NULL DEFAULT NULL PRIMARY KEY,
  Quan INTEGER NULL DEFAULT 0,
  Type_mes_q INTEGER NULL DEFAULT NULL);
"""


# Вставка параметров в таблицу Parsing
def insert_param_pars(Name_FULL, Type_mes, File_path, Line_num_file, Time_m, Cause, Prefix, Message, Num_str):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(db_name)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_insert_with_param = """INSERT INTO Parsing
                                      (  Name_FULL,Type_mes ,File_path ,Line_num_file ,Time_m , Cause ,  Prefix ,  Message,  Num_str)
                                      VALUES (?, ?, ?,?,?,?,?,?,?);"""
        data = (Name_FULL, Type_mes, File_path, Line_num_file, Time_m, Cause, Prefix, Message, Num_str)
        cursor.execute(sqlite_insert_with_param, data)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу Parsing")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# Вставка параметров в таблицу Quantity
def insert_quant(Name_f, Type_mes_q):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect(db_name)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_check = """
        SELECT Name FROM Quantity
        WHERE Name=?;
        """
        sqlite_incr = '''
                                UPDATE Quantity
                                SET Quan = Quan+1
                                WHERE Name = ?;
                                '''
        if cursor.execute(sqlite_check, (str(Name_f),)).fetchone() is None:
            sqlite_insert_quant = """   INSERT INTO Quantity
                                      ( Name,Type_mes_q)
                                      VALUES (?, ?);
                                      """
            data_q = (str(Name_f), Type_mes_q)
            cursor.execute(sqlite_insert_quant, data_q)
            cursor.execute(sqlite_incr, (str(Name_f),))
        else:
            cursor.execute(sqlite_incr, (str(Name_f),))
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу Quantity")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        print(Name_f, Type_mes_q)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# Парсинг логфайла и вствка данных
def parsing_file(patrh_log_file):
    log_file = open(patrh_log_file, 'r')
    pars_file = open("Parsing_file " + data.strftime('%H.%M.%S %d-%m-%Y') + ".log", "a+")

    type_mes = Word("UVM_" + alphas)
    file_path = Word(alphas + "/" + nums + "_" + ".")  # путь к файлу
    line_num = Suppress('(') + Word(nums) + Suppress(')')  # номер строки
    time_m = Suppress('@') + Word(' ' + nums) + Suppress(':')  # время появления сообщения в фс
    cause = Word(alphas + "." + "_" + nums + "@")  # !тут еще всякие @ _ глнянь# название тестовой последовательности
    prefix = Suppress('[') + Word(alphas + ":") + Suppress(']')  # префикс сообщения
    message = Word(
        alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + "," + "-" + "*")  # ! еще цифры в сообщении# сообщение
    text = ZeroOrMore(type_mes + file_path + line_num + time_m + cause + prefix + message)
    for num_str, line in enumerate(log_file):
        if line.startswith("UVM_INFO /") or line.startswith("UVM_WARNING /") or line.startswith(
                "UVM_ERROR /") or line.startswith("UVM_FATAL /") or line.startswith("OTHER /"):
            pr_text = text.parseString(line)
            pars_file.write(str(pr_text) + '\n')
            # Вставка отпарсенных данных в БД
            insert_param_pars(' '.join(text.parseString(line)), pr_text[0], pr_text[1], pr_text[2], pr_text[3],
                              pr_text[4],
                              pr_text[5],
                              pr_text[6], num_str)
            for i in range(7):
                insert_quant((pr_text[i],), i)
    return 'successful'


def print_pr(records_f, file):
    for row in records_f:
        file.write("ID: " + str(row[0]) + '\n')
        file.write("Строка: " + str(row[1]) + '\n')
        file.write("Тип сообщения: " + str(row[2]) + '\n')
        file.write("Путь к файлу: " + str(row[3]) + '\n')
        file.write("Номер строки в UVM: " + str(row[4]) + '\n')
        file.write("Время: " + str(row[5]) + '\n')
        file.write("Причина вызова: " + str(row[6]) + '\n')
        file.write("Префикс: " + str(row[7]) + '\n')
        file.write("Сообщение: " + str(row[8]) + '\n')
        file.write("Номер строки в лог файле: " + str(row[9]) + '\n')
        file.write("Комментарий: " + str(row[10]) + '\n')
        file.write('\n')
    return file


def print_q(records_f, file):
    file.write(
        '********************\nCправка о типе сообщений\n0 -Тип сообщения(UVM_...)\n1 -Путь к файлу\n2 -Время в фс\n3 -Номер строки в UVM файле\n4 -Причина вызова сообщения\n5 -Префикс сообщения\n6 -Сообщение\n********************\n')
    for row in records_f:
        file.write("Имя типа: " + str(row[0]) + '\n')
        file.write("Количество: " + str(row[1]) + '\n')
        file.write("Тип сообщения: " + str(row[2]) + '\n\n')
    return file

# Графический интерфейс
# Описание графического интерфеса
layout_main = [[sg.Button('Создать новую базу данных'), sg.Button('Открыть существующую базу данных')],
               [sg.Button('Выход')]]

layout_new_db = [
    [sg.Text("Введите путь к лог файлу:")], [sg.Input()], [sg.Text("Введите название теста:")], [sg.Input()],
    [sg.Button("Загрузить в новую БД отпарсенный файл")], [sg.Button("Выход")]]
layout_way_db = [
    [sg.Text("Введите путь к БД:")], [sg.Input()],
    [sg.Button("Подключить БД")], [sg.Button("Выход")]]

layout_task = [
    [sg.Button("Вывод статистики")], [sg.Button("Поиск по времени")],
    [sg.Button("Работа с комментариями")], [sg.Button("Фильтрация журнала")], [sg.Button("Выход")]]
layout_time = [
    [sg.Text("Введите время:")], [sg.Input()],
    [sg.Button("Поиск")], [sg.Button("Выход")]]
layout_com = [[sg.Text("Введите комментарий:")],
              [sg.Input()], [sg.Text("Введите номер строки в логфайле:")], [sg.Input()], [sg.Button("Добавить")],
              [sg.Button("Вывести все строки с комментариями")], [sg.Button("Выход")]]
layout_filt = [
    [sg.Button("Фильтровать по типам")],
    [sg.Button("Фильтровать по номерам строки в файле")],
    [sg.Text("Диапазон времени")], [sg.Text("Введите от какого времени")], [sg.Input()],
    [sg.Text("Введите до какого времени")], [sg.Input()], [sg.Button("Фильтровать по диапозону времени")],
    [sg.Button("Выход")]]

# Create the first Window
window = sg.Window('Главная', layout_main)
fl_win_new_db = False
fl_win_way_db = False
fl_win_task = False
fl_win_time = False
fl_win_com = False
fl_win_filt = False
# Открытие графического интерфейса
while True:
    event1, values1 = window.read()
    if event1 in (sg.WIN_CLOSED, 'Выход'):
        # User closed the Window or hit the Cancel button
        if not fl_win_new_db:
            if not fl_win_task:
                break

    if not fl_win_new_db and event1 == 'Создать новую базу данных':
        fl_win_new_db = True
        win_new_db = sg.Window("Новая БД", layout_new_db)
        window.close()
    if not fl_win_new_db and event1 == 'Открыть существующую базу данных':
        fl_win_way_db = True
        win_way_db = sg.Window("Существующая БД", layout_way_db)
        window.close()
    if fl_win_new_db:
        ev_new_db, val_new_db = win_new_db.Read()
        if ev_new_db in ('Выход', sg.WIN_CLOSED):
            fl_win_new_db = False
            win_new_db.close()
        if not fl_win_task and ev_new_db == 'Загрузить в новую БД отпарсенный файл':
            # Создание БД
            db_name = str(val_new_db[1]) + " " + data.strftime('%H.%M.%S %d-%m-%Y') + ".sqlite"  # Создание БД
            connection = create_connection(db_name)  # Подключение к БД
            execute_query(connection, create_table_pars)  # Создание таблицы Parsing
            execute_query(connection, create_table_quant)  # Создание таблицы Quntity
            parsing_file(val_new_db[0])  # Парсинг логфайла и вставка в таблицы
            # Преобразование таблицы
            with open('Transformation.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.executescript(sql_script)
            db.commit()
            db.close()

            window = sg.Window("Задачи", layout_task)
            win_task = window
            fl_win_task = True
            win_new_db.close()
    if fl_win_way_db:
        ev_way_db, val_way_db = win_way_db.Read()
        if ev_way_db in ("Выход', sg.WIN_CLOSED"):
            fl_win_way_db = False
            win_way_db.close()
        if ev_way_db == 'Подключить БД':
            db_name = val_way_db[0]
            connection = create_connection(db_name)  # Подключение к БД
            fl_way_db = False
            win_way_db.close()
            window = sg.Window("Задачи", layout_task)
            win_task = window
            fl_win_task = True
    if fl_win_task:
        ev_task, val_task = win_task.Read()
        if ev_task in ('Выход', sg.WIN_CLOSED):
            fl_win_task = False
            win_task.close()
        if ev_task == 'Вывод статистики':
            # sql вывод статистики
            with open('Statistics_parsing.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute(sql_script)
            stat_file = open("Statistics_parsing " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt", "a+")
            print_pr(cursor.fetchall(), stat_file)
            stat_file.close()
            db.commit()
            with open('Statistics_quantity.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute(sql_script)
            q_file = open("Statistics_quary " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt", "a+")
            print_q(cursor.fetchall(), q_file)
            q_file.close()
            db.close()
            win_task.close()
            fl_win_task = False
            win_task.close()
        if ev_task == 'Поиск по времени':
            window = sg.Window("Время", layout_time)
            win_time = window
            fl_win_time = True
            win_task.close()
            fl_win_task = False
        if ev_task == 'Работа с комментариями':
            window = sg.Window("Комментарий", layout_com)
            win_com = window
            fl_win_com = True
            win_task.close()
            fl_win_task = False
        if ev_task == 'Фильтрация журнала':
            window = sg.Window("Фильтрация", layout_filt)
            win_filt = window
            fl_win_filt = True
            win_task.close()
            fl_win_task = False
    if fl_win_time:
        ev_time, val_time = win_time.Read()
        if ev_time in ('Выход', sg.WIN_CLOSED):
            fl_win_time = False
            win_time.close()
        if ev_time == 'Поиск':
            # sql Поиск по времени c val_time[0]
            with open('Search_time.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            d = [val_time[0], val_time[0]]
            cursor.execute(sql_script, d)
            time_file = open("Search Time " + data.strftime('%d-%m-%Y %H.%M.%S') + ' ' + str(val_time[0]) + ".txt",
                             "a+")
            print_pr(cursor.fetchall(), time_file)
            time_file.close()
            db.commit()
            db.close()
        fl_win_time = False
        win_time.close()
    if fl_win_com:
        ev_com, val_com = win_com.Read()
        if ev_com in ('Выход', sg.WIN_CLOSED):
            fl_win_com = False
            win_com.close()
        if ev_com == 'Вывести все строки с комментариями':
            # sql Вывод всех с комментами
            with open('Print_com.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute(sql_script)
            com_file = open("All with Comments " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt",
                            "a+")
            print_pr(cursor.fetchall(), com_file)
            com_file.close()
            db.commit()
            db.close()
            fl_win_com = False
            win_com.close()
        if ev_com == 'Добавить':
            # sql Добавление коментария
            with open('Add_com.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            d = [val_com[0], val_com[1]]
            cursor.execute(sql_script, d)
            db.commit()
            db.close()
            fl_win_com = False
            win_com.close()
    if fl_win_filt:
        ev_filt, val_filt = win_filt.Read()
        if ev_filt in ('Выход', sg.WIN_CLOSED):
            fl_win_filt = False
            win_filt.close()
        if ev_filt == 'Фильтровать по типам':
            with open('Filter by Types.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute(sql_script)
            fil_type_file = open("Filter by types " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt",
                                 "a+")
            print_q(cursor.fetchall(), fil_type_file)
            fil_type_file.close()
            db.commit()
            db.close()
            fl_win_filt = False
            win_filt.close()

        if ev_filt == 'Фильтровать по номерам строки в файле':
            with open('Filter by Num_str.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute(sql_script)
            fil_nstr_file = open("Filter by Num_str " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt",
                                 "a+")
            print_pr(cursor.fetchall(), fil_nstr_file)
            fil_nstr_file.close()
            db.commit()
            db.close()
            fl_win_filt = False
            win_filt.close()
        if ev_filt == 'Фильтровать по диапозону времени':
            with open('Filter by Range.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            d = [val_filt[0], val_filt[1]]
            cursor.execute(sql_script, d)
            fil_range_file = open("Filter by Range " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt",
                                 "a+")
            print_pr(cursor.fetchall(), fil_range_file)
            fil_range_file.close()
            db.commit()
            db.close()
            fl_win_filt = False
            win_filt.close()

    time.sleep(1)