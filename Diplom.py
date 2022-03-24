import pyparsing

file = open("Test.log", 'r')
# file = open(input("Введите путь к файлу: "))#выбор журнала для загрузки
# Анализ и разбор сообщений журнала.
for line in file:
    print(line, end='')

type_mes = World(['UVM_INFO', 'UVM_WARNING', ' UVM_ERROR', 'UVM_FATAL', 'OTHER'])
file_path = World(alphas + ":" + "/")  # путь к файлу
line_num = World("(" + nums + ")")  # номер строки
time = World("@" + nums + ":")  # время появления сообщения в фс
cause = World(alphas)  # !тут еще всякие @ _ глнянь# название тестовой последовательности
prefix = World("[" + alphas + "]")  # префикс сообщения
message = World(alphas)  # ! еще цифры в сообщении# сообщение
table = type_mes + file_path + line_num + time + cause + prefix + message  # таблица со всеми данными
