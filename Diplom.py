from pyparsing import Word, Literal, alphas, nums, Optional

# file = open("Test.log", 'r')
# file = open(input("Введите путь к файлу: "))#выбор журнала для загрузки
# Анализ и разбор сообщений журнала.
# for line in file:
#    print(line, end='')
test = [
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 8898000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'fff",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 8898000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'fff",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserVirtualSeqLib.sv(404) @ 43702000: uvm_test_top.ApbSve0.vs@@myEfuseRegisterRWTestSeq [myEfuseRegisterRWTestSeq] REG RW TEST: OK. Written data: 00000000, read data: 00000000 (sign bits mask: 0x)",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 6289458000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'38",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 10732858000: uvm_test_top.ApbSve0.myUvmEnv.activeMaster.monitor [MONITOR] Ended WRITE Transfer: Address = h'0  Data = h'300002a",
    "UVM_WARNING /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 10732858000: uvm_test_top.ApbSve0.myUvmEnv.activeMaster.monitor [MONITOR] Ended WRITE Transfer: Address = h'0  Data = h'300002a"]
type_mes = Word("UVM_INFO" + "UVM_WARNING" + "UVM_ERROR" + "UVM_FATAL" + "OTHER")
file_path = Word(alphas + "/" + nums + "_" + ".")  # путь к файлу
line_num = Word("(" + nums + ")")  # номер строки
time = Word(" " + "@" + nums + ":")  # время появления сообщения в фс
cause = Word(alphas + "." + "_" + nums + "@")  # !тут еще всякие @ _ глнянь# название тестовой последовательности
prefix = Word("[" + alphas + "]")  # префикс сообщения
message = Word(alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + ",")  # ! еще цифры в сообщении# сообщение
table = type_mes + file_path + line_num + time + cause + prefix + message
for t in test:
    print(table.parseString(t))