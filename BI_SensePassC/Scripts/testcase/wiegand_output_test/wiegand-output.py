#coding=utf-8
import paramiko
import time
import random
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig

'''
此脚本仅用于韦根发测试
'''

if __name__ == '__main__':
    # 获取配置文件内容
    yamlconfig_obj = DataGetConfig()
    yamlConfig = yamlconfig_obj.getConfig('wiegandOutput.yaml')
    # print('yamlconfig: ', yamlConfig)
    host_ip = yamlConfig['Host_IP']
    # print(host_ip)
    ssh_name = yamlConfig['SSH_Name']
    ssh_pwd = yamlConfig['SSH_Password']
    # print(ssh_pwd)
    ssh_port = yamlConfig['SSH_Port']
    # print(ssh_port)

    ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
    for i in range(1,100001):
        print('————————test %s'%i)
        ssh_obj.connects()
        # 按照顺序执行wiegandOutput.yaml文件中的命令
        open_card_info = ssh_obj.send_data(yamlConfig.get('open_card_cmd'))
        # print(yamlConfig.get('open_card_cmd'))
        ssh_obj.send_data(yamlConfig['write_data_cmd'])
        # print(yamlConfig.get('write_data_cmd'))
        ssh_obj.send_data(yamlConfig.get('close_card_cmd'))
        # print(yamlConfig.get('close_card_cmd'))
        ssh_obj.disconnect()
        # os._exit()
        

        

