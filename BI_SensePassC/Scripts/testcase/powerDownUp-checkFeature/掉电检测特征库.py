#!/usr/bin/python
#coding=utf-8
from BI_SensePassC.Scripts.Sharedscript.ShareedSSH import SSH
from BI_SensePassC.Scripts.Sharedscript.SharedGetYamlConfigData import DataGetConfig
from BI_SensePassC.Scripts.Sharedscript.SharedSerial import switch_control
from BI_SensePassC.Scripts.Sharedscript.SharedSerial import Serial
from BI_SensePassC.Scripts.Sharedscript.SharedSerial import Ser_Contrl
import time
import random


if __name__ == '__main__':

    #获取配置文件
    yamlconfig_obj = DataGetConfig()
    yamlConfig = yamlconfig_obj.getConfig('Command.yaml')
    host_ip = yamlConfig.get('Host_IP')
    ssh_name = yamlConfig.get('SSH_Name')
    ssh_pwd = yamlConfig.get('SSH_Password')
    ssh_port = yamlConfig.get('SSH_Port')
    md5_feature = yamlConfig.get('original_feature_db_md5')
    com1 = yamlConfig.get('Command1')
    testMax = 10000
    ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
    ser = Ser_Contrl('com7', 9600)
    for i in range(1, testMax+1):
        print('————————test No.%s'%i)

        ser.disconnect_power()
        ramdom_time = random.randrange(80, 90)
        time.sleep(ramdom_time)

        ssh_obj.connects()
        exec_command_feedback = ssh_obj.send_data(com1)
        print('feature_db md5： ', exec_command_feedback)
        print('md5: ', md5_feature)
        flag = exec_command_feedback.find(md5_feature)
        if flag == -1:
            print('特征库md5值已经发生改变')
            break
        else:
            ssh_obj.disconnect()
            ser.connect_power()


