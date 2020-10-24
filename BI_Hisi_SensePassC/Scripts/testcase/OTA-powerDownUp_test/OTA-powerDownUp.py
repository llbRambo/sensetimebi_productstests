import time, random, sys
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
from sensetimebi_productstests.Sharedscript.logger import Logger

if __name__ == '__main__':
    testMax = 10000
    logpath = sys.path[0] + '\\log.txt'
    log = Logger(logpath, level='debug')  # 保存脚本运行log
    ser = SingleRelay('com33', 9600)
    for i in range(1, testMax+1):
        log.logger.debug('————————test No.%s————————'%i)
        ser.disconnect_power()
        ramdom_time = random.randrange(36, 120)
        time.sleep(ramdom_time)
        ser.connect_power()
