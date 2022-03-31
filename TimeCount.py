import time
from  pyparsing import *

start = time.monotonic()
#Text program start

file = open("xrun_random_test.log", 'r')

#file = open("xrun_register_rw.log", 'r')
#file = open("test.log", 'r')
type_mes = Word("UVM_INFO" + "UVM_WARNING" + "UVM_ERROR" + "UVM_FATAL" + "OTHER")

file_path = Word(alphas + "/" + nums + "_" + ".")  # путь к файлу
line_num = Suppress('(') + Word(nums) + Suppress(')')  # номер строки
time_m = Suppress('@') + Word(' ' + nums) + Suppress(':')  # время появления сообщения в фс
cause = Word(alphas + "." + "_" + nums + "@")  # !тут еще всякие @ _ глнянь# название тестовой последовательности
prefix = Suppress('[') + Word(alphas + ":") + Suppress(']')  # префикс сообщения
message = Word(alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + "," + "-" + "*")  # ! еще цифры в сообщении# сообщение
text = ZeroOrMore(type_mes + file_path + line_num + time_m + cause + prefix + message)
for line in file:
    if line.startswith("UVM_INFO /") or line.startswith("UVM_WARNING /") or line.startswith(
            "UVM_ERROR /") or line.startswith("UVM_FATAL /") or line.startswith("OTHER /"):
        pr = text.parseString(line)

#Text program end
result = time.monotonic() - start
print("Program time: {:>.3f}".format(result) + " seconds.")
