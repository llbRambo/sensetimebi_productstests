import serial,time,random

class ser_reboot(object):
    def __init__(self,port):
        # 打开端口
        self.port = serial.Serial(port=port, baudrate=9600,timeout=2)

    # 发送指令的完整流程
    def send_cmd(self, commd):
        self.port.write(commd)
        time.sleep(0.02)

    def disconnect_power(self):
        disconnect_1 = bytes([160, 1, 1, 162])  # A0 01 01 A2    第一路断电
        disconnect_2 = bytes([160, 2, 1, 163])  # A0 02 01 A3    第二路断电
        self.send_cmd(disconnect_1)
        time.sleep(0.05)
#        self.send_cmd(disconnect_2)
#        time.sleep(0.05)

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

if __name__ == '__main__':
    we_power_1 = ser_reboot(port="COM20") # 连接继电器
#    we_power_2 = ser_reboot(port="COM78") # 连接继电器
    we_powers = [we_power_1]
    i = 0
    testmax = 10000
    while i<testmax:
        wait_times = we_power_1.wait_time()
        for we_power in we_powers:
            we_power.disconnect_power()  # 关闭电源
            print("第 %s 次断开"%i)
        time.sleep(120)
        for we_power in we_powers:
            we_power.connect_power()  # 打开电源
            print("第 %s 次闭合"%i)
        time.sleep(0.3)
       #print("当前随机时间：%s,运行：%s次"%(wait_times,i))
        print("------------------------------")
        i += 1
