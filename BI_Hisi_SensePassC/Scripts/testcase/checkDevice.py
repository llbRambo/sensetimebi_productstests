from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.ShareedSSH import SCP
import time
import os, sys

def chooseProject():
    while True:
        print('***************************************************************')
        print('1.SensePass X \t 2.SensePass C')
        print('***************************************************************')
        projectnum = input('请选择以上项目序号：')
        if projectnum == '1':
            pwd = 'BI_SensePassXS#'
            return pwd
        elif projectnum == '2':
            pwd = 'BI_SensePassC#'
            return pwd
        else:
            print('输入错误！！！')

def recordInfo(ssh_obj, scp_obj):
    fileprefix = time.strftime('%Y%m%d-%H%M%S')
    filename = str(fileprefix) + '.txt'
    comlist = ['echo "***************************************************************" >> /data/',
               'fw_printenv |grep device_sn >> /data/',
               'echo "***************************************************************" >> /data/',
               'df -h /data >> /data/',
               'echo "***************************************************************" >> /data/',
               'cat /etc/product_info >> /data/',
               'echo "***************************************************************" >> /data/',
               'ps |grep service >> /data/',
               'echo "***************************************************************" >> /data/',
               'ps |grep app >> /data/',
               'echo "***************************************************************" >> /data/',
               'cat /data/process_monitor.log  >> /data/',
               'echo "***************************************************************" >> /data/'
            ]
    for line in comlist:
        line1 = line + str(filename)
        print(line1)
        ssh_obj.send_data(line1)
    cur_path = sys.path[0]
    scp_obj.singFile_download(filename, '/data/', cur_path)


if __name__ == '__main__':

    host_ip = input('请输入IP地址：')
    # print(host_ip)
    ssh_port = 22
    ssh_name = 'root'
    ssh_pwd = chooseProject()
    # print(ssh_pwd)

    ssh_obj = SSH(host_ip,ssh_port,ssh_name,ssh_pwd)
    scp_obj = SCP(host_ip, ssh_port, ssh_name, ssh_pwd)
    ssh_obj.connects()
    recordInfo(ssh_obj, scp_obj)

    # 上传文件到remote_path路径
    # scp_obj.singleFile_upload(filename, local_path, remote_path)
    #
    # # 按照顺序执行yaml文件中的命令
    # ssh_obj.connects()
    # ssh_obj.send_data('')
    # # print(yamlConfig['Command1'])
    # ssh_obj.send_data(''
    # # print(yamlConfig['Command2'])
    # ssh_obj.send_data('')
    # # print(yamlConfig['Command3'])
    # ssh_obj.send_data('')
    # # print(yamlConfig['Command4'])
    # ssh_obj.send_data('')
    # # print(yamlConfig['Command5'])
    # ssh_obj.send_data('')
    # # print(yamlConfig['Command6'])
    # ssh_obj.disconnect()