from pyparsing import *
import datetime
import sqlite3
from sqlite3 import *


# SQL
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Подключение к SQLite БД успешно")
    except Error as e:
        print(f"Ошибка при подключении к SQLite БД: '{e}'")

    return connection


def execute_query(connection, query):
    curs = connection.cursor()
    try:
        curs.execute(query)
        connection.commit()
        print("Запрос выполнен успешно")
    except Error as e:
        print(query)
        print(f"Ошибка при запросе: '{e}'")


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
  FOREIGN KEY (Type_mes) REFERENCES Quantity(Name));
"""
create_table_quant = """
CREATE TABLE Quantity (  
  Name VARCHAR NULL DEFAULT NULL PRIMARY KEY,
  Quan INTEGER NULL DEFAULT 0,
  Type_mes_q INTEGER NULL DEFAULT NULL);
"""
# Создание БД
connection = create_connection("DB_Diplom.sqlite")
execute_query(connection, create_table_quant)
execute_query(connection, create_table_pars)


def insert_param_pars(Name_FULL, Type_mes, File_path, Line_num_file, Time_m, Cause, Prefix, Message, Num_str):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect('DB_Diplom.sqlite')
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


def insert_quant(Name_f, Type_mes_q):
    global sqlite_connection
    try:
        sqlite_connection = sqlite3.connect('DB_Diplom.sqlite')
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
        print(Name_f,Type_mes_q)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


# log_file = open("xrun_random_test.log", 'r')
# log_file = open("test.log", 'r')
log_file = open("xrun_register_rw.log", 'r')

data = datetime.datetime.today() - datetime.timedelta(1)
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
d = {}
for num_str, line in enumerate(log_file):
    if line.startswith("UVM_INFO /") or line.startswith("UVM_WARNING /") or line.startswith(
            "UVM_ERROR /") or line.startswith("UVM_FATAL /") or line.startswith("OTHER /"):
        pr_text = text.parseString(line)
        pars_file.write(str(pr_text) + '\n')
        """
        print('!Name_FULL =', text.parseString(line), '!Type_mes =', pr_text[0], '!File_path =', pr_text[1],
              '!Line_num_file =', pr_text[2], ' !Time_m=', pr_text[3], '!Cause =',pr_text[4], '!Prefix =',pr_text[5],
              '! Message =',pr_text[6], '!Номер строки в реал файле =',num_str)
        """
        insert_param_pars(' '.join(text.parseString(line)), pr_text[0], pr_text[1], pr_text[2], pr_text[3], pr_text[4],
                          pr_text[5],
                          pr_text[6], num_str)
        for i in range(7):
            insert_quant((pr_text[i],), i)
        """
        fl = 0 
        for i in range(6):
            for j in d.copy(): 
                if pr_text[i] == j:
                    d[j][1] += 1
                    fl = 1
                    break
            if fl == 0:
                d.update({pr_text[i]: [i, 1]})
            fl = 0
#Вывод статистики - какие сообщения, их тип и сколько их всего
for key, val in d.items():
    print('Сообщение: ', key, 'Тип: ', val[0], 'Встретилось: ', val[1],' раз')
"""


# Поиск по журналу
def search_word(file, word):
    word = str(word)
    arr_row = []
    for row, line in enumerate(file):
        if word in line:
            arr_row.append(row + 1)
    if arr_row == []:
        return 'Значение остутсвует в файле'
    return arr_row
# Поиск по ближайшему по времени
# Добавление комментария
# Красивый интерфейс
# ! не забудь вывод красивый (дата, номер теста и тд)
