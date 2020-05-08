#!/user/bin/python
#coding=utf-8
import os
import sys
import time
import datetime
import sys
import socket
import datetime
import paramiko
import time
class hisi_ssh(object):
    # 初始化参数
    def __init__(self, host, port, username, passwd):
        self.__host = host
        self.__port = 22
        self.__username = username
        self.__passwd = passwd

    def connects(self):
        # 连接服务器
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = self.__host, port = self.__port, username = self.__username, password = self.__passwd)

    def disconnect(self):
        # 断开服务器
        self.ssh.close()
        

    def send_data(self, data):
        # 执行对应命令
        stdin, stdout, stderr = self.ssh.exec_command(data)
        return stdout

#TCP = SOCK_STREAM
#UDP = socket.SOCK_DGRAM
#iplist = ['192.168.1.101','192.168.1.103','192.168.1.104','192.168.1.105','192.168.1.106','192.168.1.107','192.168.1.108']
iplist = ["192.168.1.102"]
port = 10000
TEST_MAX = 10000
ssh_port= 22
login_name = "root"
login_pwd = "123456"
test_cmd = "reboot -f"
sn_count = 0
otp_count = 0
sn_list = []
otp_list = []
sn = "0123215CFF4A5816EE"  #每台设备不一样需要
otp = "SensePass C"
slug_cmd_sn = "AT+ATSHA204A\r\n"
slug_cmd_otp = "AT+otp\r\n"


for i in range(1, TEST_MAX+1):
    date = datetime.datetime.now()
    print("-------------------- Test "+ str(i) +"---------------------------------")
    print(date)
    for ip in iplist:
        print(ip)
        try:
            ss = hisi_ssh(ip, ssh_port, login_name, login_pwd)
            ss.connects()
            ss.send_data(test_cmd)
            time.sleep(60)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建一个socket
            sock.connect((ip,port))
            for j in range(1,6):
                print(slug_cmd_sn)
                sock.send(slug_cmd_sn.encode())
                result = sock.recv(1024).decode('utf-8')
                print(result)
                r=result.split("\n")
                s_result = r[0].split(": ")[1].strip()
                sn_result = s_result[0:]
                if sn_result == "7":
                    print("加密芯片sn号读取失败")    
                elif sn_result == sn:
                    sn_count = sn_count + 1
                else:
                    print("加密芯片sn号读取错误")
                    sn_list.append(sn_result)
                    
                print(slug_cmd_otp)
                sock.send(slug_cmd_otp.encode())
                result = sock.recv(1024).decode('utf-8')
                print(result)
                r=result.split("\n")
                o_result = r[0].split(": ")[1].strip()
                otp_result = o_result[0:]
                if otp_result == "7":
                    print("加密芯片otp号读取失败")
                elif otp_result == otp :
                    otp_count = otp_count + 1
                else:
                    print("加密芯片otp号读取错误")
                    otp_list.append(otp_result)
                print("---------------------")
            sock.close()
            print("AT+ATSHA204成功次数为："+str(sn_count))
            print("AT+otp成功次数为："+str(sn_count))   
            sock.close()
        except:
            pass
        
