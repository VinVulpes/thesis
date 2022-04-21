from pyparsing import *

log_file = open("xrun_register_rw.log", 'r') # файл журнала, который нужно проанализировать
pars_file = open("Parsing_file.txt", "a+") # файл в который записывается результат синатксического анализа

type_mes = Word("UVM_" + alphas) # тип сообщения
file_path = Word(alphas + "/" + nums + "_" + ".")  # путь к файлу
line_num = Suppress('(') + Word(nums) + Suppress(')')  # номер строки
time_m = Suppress('@') + Word(' ' + nums) + Suppress(':')  # время появления сообщения в фс
cause = Word(alphas + "." + "_" + nums + "@")  # название тестовой последовательности
prefix = Suppress('[') + Word(alphas + ":") + Suppress(']')  # префикс сообщения
message = Word(
    alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + "," + "-" + "*")  # сообщение
text = ZeroOrMore(type_mes + file_path + line_num + time_m + cause + prefix + message) # собранный текст
for line in log_file:
    pr_text = text.parseString(line)
    if len(pr_text) != 0:
        pars_file.write(str(pr_text) + '\n')
