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
table= '''
CREATE TABLE test(id integer primary key AUTOINCREMENT
                , page varchar(10)
                , dp_record_id integer
                , webserver_id integer
                , foreign key (webserver_id) REFERENCES target_dp(id));
'''

connection = create_connection("Proba.sqlite")
execute_query(connection, table)