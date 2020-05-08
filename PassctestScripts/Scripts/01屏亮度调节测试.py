#coding=utf-8
import paramiko
import time
import random
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
if __name__ == '__main__':

    iplist = ["10.9.96.199","10.9.96.47","10.9.97.172"]
    port = 22
    login_name = "root"
    login_pwd = "BI_SensePassC#"

#   test_cmd = "source /etc/profile; ubus call system info"
#   test_cmd = r"/data/mcu_test v"
    for i in range(3000):
        for ip in iplist:
            ss = hisi_ssh(ip, port, login_name, login_pwd)
            ss.connects()
            print("----------test："+str(i)+"-----------")
            print(ip)
            brightness = random.randint(0,255)
            print("当前亮度值为：" + str(brightness))
            lcd_cmd = "echo " + str(brightness) + " > /sys/class/leds/lcd_bl/brightness"
            print(lcd_cmd)
            print(ss.send_data(lcd_cmd) )
            time.sleep(3)
            ss.disconnect()

