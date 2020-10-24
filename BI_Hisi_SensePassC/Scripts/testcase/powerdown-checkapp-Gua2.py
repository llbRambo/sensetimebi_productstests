#!/usr/bin/python
#coding=utf-8
import sys, time, os
import paramiko
from scp import SCPClient
import serial

class SSH(object):
    # 初始化参数
    def __init__(self, host, port, username, passwd):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__passwd = passwd
        self.__stdin = ''
        self.__stdout = ''
        self.__stderr = ''
        self.ssh_client = paramiko.SSHClient()

    def connects(self):
        # 检查服务器是否连接
        print('########正在检查网络是否连接########')
        flag1 = 1
        flag2 = 1
        flag3 = 1
        while flag1 != -1 or flag2 != -1 or flag3 != -1:
            ping_host = 'ping ' + self.__host
            info = os.popen(ping_host).read()
            #print(info)
            target_str1 = '请求超时。'
            target_str2 = '无法访问目标主机。'
            target_str3 = '一般故障。'
            flag1 = info.find(target_str1)  #检查PC是否与设备连接上
            flag2 = info.find(target_str2)  #检查PC是否连接上网络
            flag3 = info.find(target_str3)  #检查PC是否连接上网络
            if flag1 != -1 or flag2 != -1 or flag3 != -1:
                print('        网络未连接，请连接网络        ')
        print('########网络连接成功########')

        #SSH连接设备
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname = self.__host,
                                    port = self.__port,
                                    username = self.__username,
                                    password = self.__passwd,
                                    timeout = 5)

    def disconnect(self):
        # 断开服务器
        self.ssh_client.close()


    def send_data(self, command):
        # 执行对应命令
        #print('command: %s'%command)
        # stdin, stdout, stderr = self.ssh_client.exec_command(command)  #bufsize=1024,,  timeout=70
        # return stdout.read().decode('utf-8')

        self.__stdin, self.__stdout, self.__stderr = self.ssh_client.exec_command(command)
        time.sleep(3)

    def get_data(self):
        return self.__stdout.read().decode('utf-8')


    def send_and_recv(self, command):
        shell = self.ssh_client.invoke_shell()
        shell.sendall(command)
        while 1:
            info = shell.recv(2048)
            print('info: ', info)



    # def send_data(self, command):
    #     # 执行对应命令
    #     stdin, stdout, stderr = self.ssh_client.exec_command(command)
    #     print('指令执行结果： ', stdout.read(1024).decode('utf-8'))
    #     return stdout

    def read_data(self):
        # 读取命令反馈信息
        return stdout.read().decode('utf-8')

class SerContrl(object):
    def __init__(self, port, baudrate):
        self.__port = port
        self.__baudrate = baudrate
        # 打开端口
        self.port = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=2)


    def listenport(self):
        # self.port.rs485_mode
        print(self.port.portstr, self.port.isOpen())

    # 发送指令
    def send_cmd(self, commd):
        if self.__baudrate == 115200:
            commd = commd.encode('utf-8')
            commd = commd + b' \r'
            print(commd)
            self.port.write(commd)    #Python3.x可运行，将所有str类型都转换为bytes类型
            time.sleep(0.02)
        if self.__baudrate == 9600:
            self.port.write(commd)
            time.sleep(0.02)

    # 读取指令执行后的结果
    def read_data(self):
        print('读取数据')
        # rsp = self.port.readall()
        rsp = self.port.read(2048)
        # rsp = self.port.read_all()
        print(rsp)
        # read = '\n'.join([item.rstrip('\n\r') for item in rsp])    #Python2.7x可运行
        # read = str.encode('\n').join(
        #     [item.rstrip(str.encode('\r\n')) for item in rsp])  # Python3.x可运行，将所有str类型都转换为bytes类型
        # return str(read)  # 将bytes类型转换为str类型后返回

    # 读取指令执行后的结果
    def readlines_data(self):
        print('读取数据')
        rsp = self.port.readlines()
        print(rsp)
        for i in range(len(rsp)):
            print(rsp[i])
        # read = '\n'.join([item.rstrip('\n\r') for item in rsp])    #Python2.7x可运行
        read = str.encode('\n').join([item.rstrip(str.encode('\r\n')) for item in rsp])    #Python3.x可运行，将所有str类型都转换为bytes类型 str.encode('\r\n')
        print(read)

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

    host_ip = '10.9.66.226'
    # print(host_ip)
    ssh_name = 'root'
    ssh_pwd = 'BI_SensePassC#'
    # print(ssh_pwd)
    ssh_port = 22
    we_powers = SingleRelay(port="COM44", baudrate=9600)  # 连接继电器

    for i in range(1, 1001):
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('--------------------[%s]: test No.%s--------------------' % (time1, i))
        # 此处上电，使设备开机
        we_powers.disconnect_power()
        time.sleep(60)
        ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
        ssh_obj.connects()
        ssh_obj.send_data("df -h /data")
        info_data = ssh_obj.get_data()
        print(info_data)
        # ssh_obj.send_data("ls -l /data/bi/reo/record |grep \"^-\"|wc -l")
        # info_record = ssh_obj.get_data()
        # print('/data/bi/reo/record： %s' % info_record)
        ssh_obj.send_data("ps |grep app")
        info_app = ssh_obj.get_data()
        print(info_app)
        flag_app = info_app.find('/usr/bin/sensepassx-app')
        print(flag_app)
        ssh_obj.send_data("ps |grep ai")
        info_ai = ssh_obj.get_data()
        print(info_ai)
        flat_ai = info_ai.find('ai_service')
        print(flat_ai)
        if flag_app != -1 and flat_ai != -1:
            # 服务正常，设备掉电
            # 此处掉电，使设备关机
            we_powers.connect_power()

        else:
            # 服务不正常，停止运行脚本，保留现场
            ssh_obj.disconnect()
            os._exit(1)









