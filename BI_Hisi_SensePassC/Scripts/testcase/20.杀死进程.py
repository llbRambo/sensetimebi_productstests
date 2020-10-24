#coding=utf-8
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
        

    def senddata(self, data):
        # 执行对应命令
        stdin, stdout, stderr = self.ssh.exec_command(data)
        return stdout



if __name__ == '__main__':

    host_ip = "10.9.99.7"
    port = 22
    login_name = "root"
    login_pwd = "BI_SensePassXS#"

    process_ai = "kill -9 $(pidof ai_service)"
    process_app = "kill -9 $(pidof sensepassx-app)"
    delay_time = 180
    
    test_max = 5
    print "--------------- Test kill process ---------------"
    ss = hisi_ssh(host_ip, port, login_name, login_pwd)
    ss.connects()
    for i in range(1,test_max+1):
        print "Test ", i
        ss.senddata(process_ai)
        time.sleep(delay_time)
        
        ss.senddata(process_app)
        time.sleep(delay_time)
    ss.disconnect()


