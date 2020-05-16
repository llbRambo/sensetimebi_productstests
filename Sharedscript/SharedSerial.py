#!/usr/bin/python
#coding=utf-8
#pip install pySerial
import serial
import time
import random

class SerContrl(object):
    def __init__(self, port, baudrate):
        self.__port = port
        self.__baudrate = baudrate
        # 打开端口
        self.port = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=2)

    # 发送指令
    def send_cmd(self, commd):
        if self.__baudrate == 115200:
            commd = commd + ' \r\n'
            self.port.write(str.encode(commd))    #Python3.x可运行，将所有str类型都转换为bytes类型
            time.sleep(0.02)
        if self.__baudrate == 9600:
            self.port.write(commd)
            time.sleep(0.02)

    # 读取指令执行后的结果
    def read_data(self):
        rsp = self.port.readlines()
        # read = '\n'.join([item.rstrip('\n\r') for item in rsp])    #Python2.7x可运行
        read = str.encode('\n').join([item.rstrip(str.encode('\r\n')) for item in rsp])    #Python3.x可运行，将所有str类型都转换为bytes类型
        return str(read)    #将bytes类型转换为str类型后返回

    # 关闭端口
    def close_port(self):
        try:
            self.port.close()
        except:
            print("close port fail")

class SingleRelay(SerContrl):
    def __init__(self, port, baudrate):
        SerContrl.__init__(self, port, baudrate)

    # 控制单路继电器串口
    def disconnect_power(self):
        disconnect_1 = bytes([160, 1, 1, 162])  # A0 01 01 A2    第一路断电
        self.send_cmd(disconnect_1)
        time.sleep(0.05)

    # 控制单路继电器串口
    def connect_power(self):
        connect_1 = bytes([160, 1, 0, 161])  # A0 01 00 A1       第一路上电
        self.send_cmd(connect_1)
        time.sleep(0.05)

    # 设置断电随机时间
    def wait_time(self):
        times = random.randint(1, 1)
        return times


if __name__ == '__main__':
    relay = SingleRelay('com31', 9600)
    relay.disconnect_power()
    time.sleep(2)
    relay.connect_power()



    # ser1 = SerContrl('com17', 115200)
    # # cmd_str = 'ps |grep service'.encode('utf-8') #\r\n
    # # cmd_str = bytes(cmd_str)
    # ser1.send_cmd('ubus call ai ai_db_total_count')
    # info = ser1.read_data()
    # flag = info.find('device_service')
    # print(info)
    # # if flag != -1:
    # #     print('恭喜，已找到！！！！')

