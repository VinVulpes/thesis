if ev_filt == 'Фильтровать по названию':
    with open('Filter by Custom, type = ' + val_filt[0] + '.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(sql_script, [val_filt[1]])
    fil_cust_file = open("Filter by Custom " + data.strftime('%d-%m-%Y %H.%M.%S') + ".txt",
                         "a+")
    print_pr(cursor.fetchall(), fil_cust_file)
    fil_cust_file.close()
    db.close()
    fl_win_filt = False
    win_filt.close()

    layout_filt = [
        [sg.Button("Фильтровать статистику по типам")],
        [sg.Button("Фильтровать статистикупо номерам строки в файле")], [sg.Text("Введите название типа сообщения:")],
        [sg.Input()], [sg.Text("Введите название сообщения")], [sg.Input()], [sg.Button("Фильтровать по названию")],
        [sg.Button("Выход")]]