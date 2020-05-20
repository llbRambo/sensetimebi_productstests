#!/usr/bin/python
#coding=utf-8
import os
import sys
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.ShareedSSH import SCP
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig

if __name__ == '__main__':

    #获取配置文件内容
    yamlconfig_obj = DataGetConfig()
    yamlConfig = yamlconfig_obj.getConfig('Mcu_upgrade_command.yaml')
    print('yamlconfig: ', yamlConfig)
    host_ip = yamlConfig['Host_IP']
    print(host_ip)
    ssh_name = yamlConfig['SSH_Name']
    ssh_pwd = yamlConfig['SSH_Password']
    print(ssh_pwd)
    ssh_port = yamlConfig['SSH_Port']
    print(ssh_port)
    #获取脚本当前所在路径
    local_path = sys.path[0]
    remote_path = '/data/'

    filename = 'wirte.sh'

    ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
    scp_obj = SCP(host_ip, ssh_port, ssh_name, ssh_pwd)
    # 上传文件
    scp_obj.singleFile_upload(filename, local_path, remote_path)
    #按照顺序执行命令
    ssh_obj.connects()
    ssh_obj.send_data(yamlConfig['Command1'])
    print(yamlConfig['Command1'])
    ssh_obj.send_data(yamlConfig['Command2'])
    print(yamlConfig['Command2'])
    ssh_obj.send_data(yamlConfig['Command3'])
    print(yamlConfig['Command3'])
    ssh_obj.disconnect()

    #os._exit()




