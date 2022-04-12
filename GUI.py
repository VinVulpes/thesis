import PySimpleGUI as sg
import time

# Create some Elements
new_bd_btn = sg.Button('Создать новую базу данных')
ex_bd_btn = sg.Button('Открыть существующую базу данных')
exit_btn = sg.Button('Выход')
layout_main = [[new_bd_btn, ex_bd_btn], [exit_btn]]

layout_new_db = [
    [sg.Text("Введите путь к лог файлу:")], [sg.Input()],[sg.Text("Введите название теста:")], [sg.Input()],
    [sg.Button("Загрузить в новую БД отпарсенный файл")], [sg.Button("Выход")]]
layout_way_db = [
    [sg.Text("Введите путь к БД:")], [sg.Input()],
    [sg.Button("Подключить БД")], [sg.Button("Выход")]]

layout_task = [
    [sg.Button("Вывод статистики")], [sg.Button("Поиск по времени")],
    [sg.Button("Работа с комментариями")], [sg.Button("Выход")]]
# [sg.Text("Добавление комментария (введите номер строки)")],[sg.Input()],
layout_time = [
    [sg.Text("Введите время:")], [sg.Input()],
    [sg.Button("Поиск")], [sg.Button("Выход")]]
layout_com = [
    [sg.Text("Введите номер строки:")], [sg.Input()], [sg.Button("Добавить")],
    [sg.Button("Вывести все строки с комментариями")], [sg.Button("Выход")]]

# Create the first Window
window = sg.Window('Главная', layout_main)
fl_win_new_db = False
fl_win_way_db = False
fl_win_task = False
fl_win_time = False
fl_win_com = False
# Create the event loop
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
            """
            db_name_new = "DB_Diplom " + data.strftime('%H.%M.%S %d-%m-%Y') + ".sqlite"  # Создание БД
            connection = create_connection(db_name_new)  # Подключение к БД
            execute_query(connection, create_table_pars)  # Создание таблицы Parsing
            execute_query(connection, create_table_quant)  # Создание таблицы Quntity
            parsing_file(val_new_db[0]) # Парсинг логфайла и вставка в таблицы
            #!!!Привести по красоте запросом еще
            """
            window = sg.Window("Задачи", layout_task)
            win_task = window
            fl_win_task = True
            win_new_db.close()
    if fl_win_way_db:
        ev_way_db, val_way_db = win_way_db.Read()
        if ev_way_db in ('Выход', sg.WIN_CLOSED):
            fl_win_way_db = False
            win_way_db.close()
        if ev_way_db == 'Подключить БД':
            # подключение библиотеки бд
            print(val_way_db[0])
            #db_name = val_way_db[0]
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
    if fl_win_time:
        ev_time, val_time = win_time.Read()
        if ev_time in ('Выход', sg.WIN_CLOSED):
            fl_win_time = False
            win_time.close()
        if ev_time == 'Поиск':
            # sql Поиск по времени c val_time[0]
            print(val_time[0])
            fl_win_time = False
            win_time.close()
    if fl_win_com:
        ev_com, val_com = win_com.Read()
        if ev_com in ('Выход', sg.WIN_CLOSED):
            fl_win_com = False
            win_com.close()
        if ev_com == 'Вывести все строки с комментариями':
            # sql Вывод всех с комментами
            fl_win_com = False
            win_com.close()
        if ev_com == 'Добавить':
            # sql Добавление коментария
            print(val_com[0])
            fl_win_com = False
            win_com.close()
    time.sleep(1)
