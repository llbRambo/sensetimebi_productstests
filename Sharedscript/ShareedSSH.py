# -*- coding: utf-8 -*-
import os
import sys

import paramiko
from scp import SCPClient


class SSH(object):
    # 初始化参数
    def __init__(self, host, port, username, passwd):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__passwd = passwd
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
        print('command: %s'%command)
        stdin, stdout, stderr = self.ssh_client.exec_command(command, bufsize=1024, timeout=10)
        #print('指令执行结果： ', stdout.read().decode('utf-8'))
        return stdout.read().decode('utf-8')

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

class SCP(SSH):
    def __init__(self, host, port, username, passwd):
        SSH.__init__(self, host, port, username, passwd)

    # 把本地某个指定文件上传到远程主机指定路径
    def singleFile_upload(self, filename, local_path, remote_path):
        self.connects()
        _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
        local_file = str(local_path) + '\\' + str(filename)
        remote_path = str(remote_path)
        _scp.put(local_file, remote_path)
        print("file " + str(local_file) + " to " + str(remote_path) + "  upload  successfully.")
        self.disconnect()

    # 把远程主机上的文件传送到本地
    def singFile_download(self, filename, remote_path, local_path):
        self.connects()
        _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
        remote_file = str(remote_path) + '/' + str(filename)
        _scp.get(remote_file, local_path)
        print("file " + str(remote_file) + " to " + str(local_path) + "  download  successfully.")
        self.disconnect()

    # # 把本地某个指定路径下的所有文件上传到远程主机指定路径
    # def Files_upload(self, local_path, remote_path):
    #     self.connects()
    #     _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
    #     _scp.put(local_path, remote_path)
    #     print("info:  upload files successfully！")
    #     self.disconnect()

    def modify_path(self, remote_path, local_path):
        self.__remote_path = remote_path
        self.__local_path = local_path


if __name__ == '__main__':
    scp = SCP('10.9.40.70', 22, 'root', 'BI_SensePassC#')
    filename = 'mcu_tools.txt'
    localpath = sys.path[0]
    remotepath = '/data'
    scp.singFile_download(filename, remotepath, localpath)