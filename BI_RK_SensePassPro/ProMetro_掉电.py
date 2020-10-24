#!/usr/bin/python
#coding=utf-8
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
import time
import random
import os

def connects(host):
    # 检查服务器是否连接
    print('########正在检查网络是否连接########')
    flag1 = 1
    flag2 = 1
    flag3 = 1
    while flag1 != -1 or flag2 != -1 or flag3 != -1:
        ping_host = 'ping ' + host
        info = os.popen(ping_host).read()
        # print(info)
        target_str1 = '请求超时。'
        target_str2 = '无法访问目标主机。'
        target_str3 = '一般故障。'
        flag1 = info.find(target_str1)  # 检查PC是否与设备连接上
        flag2 = info.find(target_str2)  # 检查PC是否连接上网络
        flag3 = info.find(target_str3)  # 检查PC是否连接上网络
        # if flag1 != -1 or flag2 != -1 or flag3 != -1:
        #      print('        网络未连接，请连接网络        ')
    print('########网络连接成功########')


if __name__ == '__main__':
    testMax = 10000
    ser = SingleRelay('com44', 9600)
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in range(1, testMax+1):
        print('————————[%s]:test No.%s'%(time1, i))
        ser.connect_power()
        #通过ping设备的静态IP：192.168.1.100来判断设备是否开机
        # connects('192.168.1.100')
        t = random.randrange(30,100)
        time.sleep(t)
        ser.disconnect_power()
        time.sleep(10)

