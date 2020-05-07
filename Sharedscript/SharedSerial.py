#!/usr/bin/python
# coding=utf-8
#pip install pySerial
import serial
import time

class Ser_Contrl(object):
    def __init__(self, port, baudrate):
        self.__port = port
        self.__baudrate = baudrate
        # 打开端口
        self.port = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=2)

    # 发送指令的完整流程
    def send_cmd(self, commd):
        self.port.write(commd)
        time.sleep(0.02)

    #控制单路继电器串口
    def disconnect_power(self):
        disconnect_1 = bytes([160, 1, 1, 162])  # A0 01 01 A2    第一路断电
        disconnect_2 = bytes([160, 2, 1, 163])  # A0 02 01 A3    第二路断电
        self.send_cmd(disconnect_1)
        time.sleep(0.05)
#        self.send_cmd(disconnect_2)
#        time.sleep(0.05)

    #控制单路继电器串口
    def connect_power(self):
        connect_1 = bytes([160, 1, 0, 161])  # A0 01 00 A1       第一路上电
        connect_2 = bytes([160, 2, 0, 162])  # A0 02 00 A2       第二路上电
        self.send_cmd(connect_1)
        time.sleep(0.05)
#        self.send_cmd(connect_2)
#        time.sleep(0.05)


    #设置断电随机时间
    def wait_time(self):
        times = random.randint(1, 1)
        return times

class Serial(object):
    def __init__(self, port, baudrate):
        self.__prot = port
        self.__baudrate = baudrate
        self.__timeout = 1
        self.__serial_obj = serial.Serial(self.__prot, self.__baudrate, timeout=float(self.__timeout))

    def write_data(self, str):
        self.__serial_obj.write(str)
        return

    def read_data(self):
        rsp = self.__serial_obj.readlines()
        return rsp

    def close_port(self):
        try:
            self.__serial_obj.close()
        except:
            print( "close port fail")


class switch_control(Serial):
    def __init__(self, port, baud):
        Serial.__init__(self, port, baud)
        # self.__delay_time = 3
        # self.__key_value = "0"
        # self.__default = "0"
        # self.__key_press_time = 1
    def switch_on(self, delay_time):
        on = "\xA0\x01\x01\xA2"
        off = "\xA0\x01\x00\xA1"
        self.__delay_time = delay_time
        # self.__serial_obj.open_port()
        self.__serial_obj.write_data(on)
        time.sleep(self.__delay_time)
        self.__serial_obj.write_data(off)
        time.sleep(3)

