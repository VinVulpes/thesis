from sqlite3 import *
import sqlite3
import PySimpleGUI as sg


def create_connection(path):  # Соединение с БД
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


sql_script = '''
SELECT * FROM Parsing'''
db_name = 'Suka2 22.38.29 20-04-2022.sqlite'
db = sqlite3.connect(db_name)
cursor = db.cursor()
cursor.execute(sql_script)
print(cursor.fetchall())
cursor.execute(sql_script)
print(cursor.fetchone())
l = []
for i in range():
    cursor.execute(sql_script)
#print(l)
contact_information_array = l
headings = ['Full Name', '1', '2','4','5','6','7','8','9']

layout = [[sg.Table(values=contact_information_array, headings=headings, max_col_width=100, auto_size_columns=True,
                    display_row_numbers=True, justification='right', num_rows=10, key='-TABLE-', row_height=35)]]

window = sg.Window("Contact Information", layout)
while True:
    event, val = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

window.close()
