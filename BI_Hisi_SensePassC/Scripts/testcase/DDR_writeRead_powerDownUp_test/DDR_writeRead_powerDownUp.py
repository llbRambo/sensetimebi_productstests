#!/usr/bin/python
#coding=utf-8
import os
import time
import random
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay

if __name__ == '__main__':

    ser = SingleRelay('com33', 9600)
    #获取配置文件内容
    yamlconfig_obj = DataGetConfig()
    yamlConfig = yamlconfig_obj.getConfig('DDR_writeRead_powerDownUp_command.yaml')
    #print('yamlconfig: ', yamlConfig)
    host_ip = yamlConfig['Host_IP']
    #print(host_ip)
    ssh_name = yamlConfig['SSH_Name']
    ssh_pwd = yamlConfig['SSH_Password']
    #print(ssh_pwd)
    ssh_port = yamlConfig['SSH_Port']
    #print(ssh_port)

    ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)

    for i in range(1591, 2001):
        print('test %s'%i)
        ser.disconnect_power()
        time_sleep = random.randrange(20, 60)
        time.sleep(time_sleep)

        # #按照顺序执行命令
        # ssh_obj.connects()
        # s1 = ssh_obj.send_data(yamlConfig['Command1'])
        # print(s1)
        # s2 = ssh_obj.send_data(yamlConfig['Command2'])
        # print(s2)
        # s3 = ssh_obj.send_data(yamlConfig['Command3'])
        # print(s3)
        # ssh_obj.disconnect()

        ser.connect_power()
        time.sleep(5)






    #os._exit()




