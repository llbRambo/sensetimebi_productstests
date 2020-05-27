#!/usr/bin/python
#coding=utf-8
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
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
    ser = SingleRelay('com33', 9600)
    for i in range(1, testMax+1):
        print('————————test No.%s'%i)

        ser.disconnect_power()
        ramdom_time = random.randrange(80, 90)
        time.sleep(ramdom_time)

        ssh_obj.connects()

        exec_command_feedback = ssh_obj.send_data(com1)
        print('feature_db md5： ', exec_command_feedback)
        print('md5: ', md5_feature)
        flag1 = exec_command_feedback.find(md5_feature)

        flag2 = ssh_obj.send_data(yamlConfig.get('Command2')).find(yamlConfig.get('original_k_feature_current_index_md5'))
        print('flag2: ', flag2)
        flag3 = ssh_obj.send_data(yamlConfig.get('Command3')).find(yamlConfig.get('original_k_feature_current_k_md5'))

        flag4 = ssh_obj.send_data(yamlConfig.get('Command4')).find(yamlConfig.get('original_k_feature_current_v_md5'))

        flag5 = ssh_obj.send_data(yamlConfig.get('Command5')).find(yamlConfig.get('original_k_feature_enroll_k_md5'))

        flag6 = ssh_obj.send_data(yamlConfig.get('Command6')).find(yamlConfig.get('original_k_feature_enroll_v_md5'))

        print('flag2: ',flag2)
        if flag1 == -1 or flag2 == -1 or flag3 == -1 or flag4 == -1 or flag5 == -1 or flag6 == -1 :
            print('特征库md5值已经发生改变')
            break
        else:
            ssh_obj.disconnect()
            ser.connect_power()


