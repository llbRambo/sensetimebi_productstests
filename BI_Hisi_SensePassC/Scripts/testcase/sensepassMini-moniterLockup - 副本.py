#!/usr/bin/python
#coding=utf-8
import sys, time, os
import paramiko
from scp import SCPClient

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
    # #5设备
    host_ip = '10.9.2.10'
    # print(host_ip)
    ssh_name = 'root'
    ssh_pwd = 'BI_SenseWe#'
    # print(ssh_pwd)
    ssh_port = 22

    for i in range(1, 1001):
        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('--------------------[%s]: test No.%s--------------------' % (time1, i))
        ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
        ssh_obj.connects()
        ssh_obj.send_data("df -h /data")
        info_data = ssh_obj.get_data()
        print(info_data)

        ssh_obj.send_data("killall app_aikey")
        time.sleep(3)
        ssh_obj.send_data("source /etc/profile; ubus -v list app.web | grep account")
        # info_app = ssh_obj.get_data()
        # print(info_app)
        # flag_app = info_app.find('account_verify')
        # print(flag_app)
        # if flag_app != -1:
        #     ssh_obj.send_data("reboot -f")
        #     time.sleep(60)
        #     connects(host_ip)
        # else:
        #     ssh_obj.disconnect()
        #     os._exit(1)









