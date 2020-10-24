#!/usr/bin/python
#coding=utf-8
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
import time
import random
import os
from sensetimebi_productstests.Sharedscript.logger import Logger


if __name__ == '__main__':
    testMax = 25
    insert_success_count = 0
    Pullout_success_count = 0
    check_flag = False
    AndroidDevice = '10.9.40.82:8888'
    log = Logger('D:\\test-project\\000-testScripts\\sensetimebi_productstests\\BI_RK_SensePassPro\\usbchecklog.txt',
                 level='debug')  # 保存脚本运行log
    ser = SingleRelay('com25', 9600)

    for i in range(1, testMax+1):
        log.logger.debug('————————test No.%s'%i)
        ser.connect_power()
        time.sleep(10)

        info = os.popen('adb -s %s shell ls /storage' % AndroidDevice).read()
        # log.logger.debug(info)
        flag = info.find('7835-637F')
        if flag != -1:
            insert_success_count += 1
            log.logger.debug('usb插入成功！！！')
            check_flag = True
        else:
            log.logger.debug('usb未插入！！！')

        log.logger.debug('插入成功率为：%s' % (insert_success_count / i))
        time.sleep(3)

        ser.disconnect_power()
        time.sleep(10)
        if check_flag:
            info = os.popen('adb -s %s shell ls /storage' % AndroidDevice).read()
            # log.logger.debug(info)
            flag = info.find('7835-637F')
            if flag != -1:
                log.logger.debug('usb未拔出！！！')
            else:
                Pullout_success_count += 1
                log.logger.debug('usb已经拔出！！！')
                check_flag = False
        log.logger.debug('拔出成功率为：%s' % (Pullout_success_count / i))
        time.sleep(3)



