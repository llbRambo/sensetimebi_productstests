# coding: utf-8

import uiautomator2 as u2
import time
import autoit
import os
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
from sensetimebi_productstests.Sharedscript.SharedAdbOperation import AdbOpt
from sensetimebi_productstests.Sharedscript.logger import Logger

if __name__ == '__main__':
    ipport = '10.9.40.25:8888'

    log = Logger('D:\\test-project\\000-testScripts\\sensetimebi_productstests\\BI_RK_SensePass020\\111.txt',
                 level='debug')  # 保存脚本运行log
    d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
    adb = AdbOpt(ipport)
    relay = SingleRelay('com37', 9600)
    for i in range(109, 2000):
        log.logger.debug('————————test:%s————————'%i)
        relay.connect_power()
        # 等待设备开机
        time.sleep(20)
        adb.adb_screencap(i, 'D:\\test-project\\009-火神mini\\不出流')
        time.sleep(1)
        relay.disconnect_power()  # 给设备上电
        time.sleep(5*60)   #给设备下电
