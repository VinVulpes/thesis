from pyparsing import *

file = open("Test.log", 'r')
'''
test = [
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 8898000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'fff",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 8898000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'fff",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserVirtualSeqLib.sv(404) @ 43702000: uvm_test_top.ApbSve0.vs@@myEfuseRegisterRWTestSeq [myEfuseRegisterRWTestSeq] REG RW TEST: OK. Written data: 00000000, read data: 00000000 (sign bits mask: 0x)",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 6289458000: uvm_test_top.ApbSve0.myUvmEnv.passiveSlave0.monitor [MONITOR] Ended WRITE Transfer: Address = h'8  Data = h'38",
    "UVM_INFO /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 10732858000: uvm_test_top.ApbSve0.myUvmEnv.activeMaster.monitor [MONITOR] Ended WRITE Transfer: Address = h'0  Data = h'300002a",
    "UVM_WARNING /home/user16/workspace/PROJ/sim/standalone_sim/cdns_apb_vip_efuse/apb_vip_src/cdnApbUvmUserMonitor.sv(76) @ 10732858000: uvm_test_top.ApbSve0.myUvmEnv.activeMaster.monitor [MONITOR] Ended WRITE Transfer: Address = h'0  Data = h'300002a"]
'''
type_mes = Word("UVM_INFO" + "UVM_WARNING" + "UVM_ERROR" + "UVM_FATAL" + "OTHER")
file_path = Word(alphas + "/" + nums + "_" + ".") # путь к файлу

line_num = Suppress('(')+Word(nums)+Suppress(')')  # номер строки
time = Suppress('@')+Word(' '+ nums)+Suppress(':')  # время появления сообщения в фс
cause = Word(alphas + "." + "_" + nums + "@")  # !тут еще всякие @ _ глнянь# название тестовой последовательности
prefix = Suppress('[')+Word( alphas)+Suppress(']')  # префикс сообщения
message = Word(alphas + ":" + "'" + nums + "." + "=" + " " + "(" + ")" + ",")  # ! еще цифры в сообщении# сообщение
text = ZeroOrMore(type_mes + file_path + line_num + time + cause + prefix + message)
print(text.parseFile(file))

