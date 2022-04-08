import datetime
db_name = "DB_Diplom"+ datetime.strftime('%H.%M.%S %d-%m-%Y') +".sqlite"
print(db_name)



#Словарь
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