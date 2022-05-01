from pyparsing import *
import sqlite3
from sqlite3 import *
import datetime

create_table_pars = """ 
CREATE TABLE Parsing (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name_FULL VARCHAR NULL DEFAULT NULL,
  Type_mes VARCHAR NULL DEFAULT NULL,
  File_path VARCHAR NULL DEFAULT NULL,
  Line_num_file VARCHAR NULL DEFAULT NULL,
  Time_m INTEGER NULL DEFAULT NULL,
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
acceleration = """
PRAGMA synchronous = OFF;
"""


def create_connection(path):  # Соединение с БД
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"Ошибка при подключении к SQLite БД: '{e}'")

    return connection


def execute_query(connection, query):  # Запрос к БД
    curs = connection.cursor()
    try:
        curs.execute(query)
        connection.commit()
    except Error as e:
        print(query)
        print(f"Ошибка при запросе: '{e}'")


def insert_param_pars(d):
    cursor = sqlite_connection.cursor()
    with open('Insert_pars.sql', 'r') as sql_file:
        sqlite_insert_with_param = sql_file.read()
    cursor.executemany(sqlite_insert_with_param, d)


# Вставка параметров в таблицу Quantity
def insert_quant(d):
    cursor = sqlite_connection.cursor()
    sqlite_check = """
            SELECT Name FROM Quantity
            WHERE Name=?;
            """
    sqlite_incr = '''
                                    UPDATE Quantity
                                    SET Quan = Quan+1
                                    WHERE Name = ?;
                                    '''
    sqlite_insert_quant = """   INSERT INTO Quantity
                                          ( Name,Type_mes_q)
                                          VALUES (?, ?);
                                          """
    for i in range(len(d)):
        if cursor.execute(sqlite_check, (str(d[i][0]),)).fetchone() is None:
            cursor.execute(sqlite_insert_quant, (str(d[i][0]), d[i][1]))
            cursor.execute(sqlite_incr, (str(d[i][0]),))
        else:
            cursor.execute(sqlite_incr, (str(d[i][0]),))


# Парсинг логфайла и вствка данных
def parsing_file(patrh_log_file):
    log_file = open(patrh_log_file, 'r')
    # pars_file = open("Parsing_file .log", "a+")

    type_mes = Word("UVM_" + alphas)  # тип сообщения
    file_path = ZeroOrMore(Word(alphanums + "/" + "_" + "."))  # путь к файлу
    line_num = ZeroOrMore((Suppress('(')) + Word(nums) + Suppress(')'))  # номер строки
    time_m = Suppress('@') + Word(' ' + nums) + Suppress(':')  # время появления сообщения в фс
    cause = Word(alphanums + "." + "_" + "@")  # название тестовой последовательности
    prefix = Suppress('[') + Word(alphas + ":" + '_') + Suppress(']')  # префикс сообщения
    message = Word(
        alphanums + ":" + "'" + "." + "=" + " " + "(" + ")" + "," + "-" + "*")  # ! # сообщение
    text = ZeroOrMore(type_mes + file_path + line_num + time_m + cause + prefix + message)
    data_par = []
    data_quant = []
    global sqlite_connection
    for num_str, line in enumerate(log_file):
        pr_text = text.parseString(line)

        if len(pr_text) != 0:
            if len(pr_text) != 7:
                pr_text.insert(1, None)
                pr_text.insert(1, None)
            # pars_file.write(str(pr_text) + '\n')
            # Вставка отпарсенных данных в БД
            data_par.append([' '.join(text.parseString(line)), pr_text[0], pr_text[1], pr_text[2], pr_text[3],
                             pr_text[4],
                             pr_text[5],
                             pr_text[6], num_str + 1])
            for i in range(7):
                data_quant.append([(pr_text[i],), i])
    try:
        sqlite_connection = sqlite3.connect(db_name)
        insert_param_pars(data_par)
        insert_quant(data_quant)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    sqlite_connection.commit()
    return 'successful'


# Создание БД
s = 0
l = []
for i in range(1):
    start_time = datetime.datetime.now()
    log_file = "C:\\Users\\mi\\Desktop\\Тесты на скорость\\Test 4, 1215919.log"
    db_name = 'Test' + str(i) + '.sqlite'  # Создание БД
    connection = create_connection(db_name)  # Подключение к БД
    execute_query(connection, acceleration)
    execute_query(connection, create_table_pars)  # Создание таблицы Parsing
    execute_query(connection, create_table_quant)  # Создание таблицы Quntity
    parsing_file(log_file)  # Парсинг логфайла и вставка в таблицы
    delta = datetime.datetime.now() - start_time
    t = delta.seconds + (delta.microseconds) / 1000000
    s += t
    l.append(t)
print(l)
print(s / 1)
