import time
from  pyparsing import *
import datetime

start = time.monotonic()
#Text program start

# log_file = open("xrun_random_test.log", 'r')
# log_file = open("test.log", 'r')
log_file = open("xrun_register_rw.log", 'r')
data = datetime.datetime.today() - datetime.timedelta(1)
pars_file = open("Parsing_file " + data.strftime('%H.%M.%S %d-%m-%Y') + ".log", "a+")

type_mes = Word("UVM_"+alphas)
file_path = Word(alphas + "/" + nums + "_" + ".")  # путь к файлу
line_num = Suppress('(') + Word(nums) + Suppress(')')  # номер строки
time_m = Suppress('@') + Word(' ' + nums) + Suppress(':')  # время появления сообщения в фс
cause = Word(alphas + "." + "_" + nums + "@")  # !тут еще всякие @ _ глнянь# название тестовой последовательности
prefix = Suppress('[') + Word(alphas + ":") + Suppress(']')  # префикс сообщения
message = Word(
    alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + "," + "-" + "*")  # ! еще цифры в сообщении# сообщение
text = ZeroOrMore(type_mes + file_path + line_num + time_m + cause + prefix + message)
d = {}
for line in log_file:
    if line.startswith("UVM_INFO /") or line.startswith("UVM_WARNING /") or line.startswith(
            "UVM_ERROR /") or line.startswith("UVM_FATAL /") or line.startswith("OTHER /"):
        pr_text = text.parseString(line)
        pars_file.write(str(pr_text)+'\n')
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

#Text program end
result = time.monotonic() - start
print("Program time: {:>.3f}".format(result) + " seconds.")
