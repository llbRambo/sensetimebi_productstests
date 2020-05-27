#!/usr/bin/python
#coding=utf-8
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
import time
import random


if __name__ == '__main__':
    testMax = 10000
    ser = SingleRelay('com33', 9600)
    for i in range(1, testMax+1):
        print('————————test No.%s'%i)
        ser.disconnect_power()
        ramdom_time = random.randrange(36, 90)
        time.sleep(ramdom_time)
        ser.connect_power()


