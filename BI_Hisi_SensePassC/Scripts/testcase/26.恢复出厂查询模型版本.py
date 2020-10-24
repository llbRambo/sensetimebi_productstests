#coding=utf-8
import paramiko
import time
import json
import re


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
        #print stderr.readlines()
        return stdout



if __name__ == '__main__':

    host_ip = "10.9.40.118"
    port = 22
    login_name = "root"
    login_pwd = "BI_SensePassXS#"
    get_model_version_cmd = "source /etc/profile; ubus -v call ai ai_db_feature_version"


    recovey_factory_cmd = "fw_setenv factory_recovery 1" 
    system_reboot = "reboot"

    print "--------------- recovey factory mode ---------------"
    ss = hisi_ssh(host_ip, port, login_name, login_pwd)
    ss.connects()
    print " recovey factory mode "
    ss.senddata(recovey_factory_cmd)
    ss.senddata(system_reboot)
    time.sleep(60)
    ss.disconnect()

    result = []
    ss = hisi_ssh(host_ip, port, login_name, login_pwd)
    ss.connects()
    result = ss.senddata(get_model_version_cmd).readlines()
    model_version = result[len(result)-2]
    model_version = json.loads(json.dumps(model_version)).lstrip() #字典转成JSON,并且去掉空格。
    print model_version
    result = re.findall(r'\d', model_version)
    time.sleep(3)
    ss.disconnect()

    


