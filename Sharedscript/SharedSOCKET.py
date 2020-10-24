#!/usr/bin/python
#coding=utf-8
import socket


class Socket(object):

    def __init__(self, client, port):
        self.__client = client
        self.__port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket

    def connect(self):
        '''
        # 检查服务器是否连接
        print('########正在检查网络是否连接########')
        flag1 = 1
        flag2 = 1
        flag3 = 1
        while flag1 != -1 or flag2 != -1 or flag3 != -1:
            ping_host = 'ping ' + self.__client
            info = os.popen(ping_host).read()
            # print(info)
            target_str1 = '请求超时。'
            target_str2 = '无法访问目标主机。'
            target_str3 = '一般故障。'
            flag1 = info.find(target_str1)  # 检查PC是否与设备连接上
            flag2 = info.find(target_str2)  # 检查PC是否连接上网络
            flag3 = info.find(target_str3)  # 检查PC是否连接上网络
            if flag1 != -1 or flag2 != -1 or flag3 != -1:
                print('        网络未连接，请连接网络        ')
        print('########网络连接成功########')
        '''
        self.sock.connect((self.__client, self.__port))

    def socket_send(self, cmd):
        # print(cmd)
        self.sock.send(cmd.encode())
        return self.sock.recv(1024).decode('utf-8')
        # return self.sock.recvfrom(2048)  # .decode('utf-8')

    def socket_read(self):
        return self.sock.recv(1024).decode('utf-8')

    def socket_close(self):
        self.sock.close()
