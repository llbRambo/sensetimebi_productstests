#!/usr/bin/python
#coding=utf-8
import time
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH

if __name__ == '__main__':
    host_ip = '192.168.1.100'
    # print(host_ip)
    ssh_name = 'root'
    ssh_pwd = 'BI_SensePassXS#'
    # print(ssh_pwd)
    ssh_port = 22
    # print(ssh_port)
    i = 1
    j = 1
    flag = 0
    print('1')
    for i in range(2500, 50001):
        print('——————————————test %s——————————————'%i)
        for j in range(1, 3):
            ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
            ssh_obj.connects()
            if flag == 0:
                print('切到工厂模式！！！')
                ssh_obj.send_data('params_rw umode 0')
                flag = 1
            elif flag == 1:
                print('切到用户模式！！！')
                ssh_obj.send_data('params_rw umode 1')
                flag = 0
            ssh_obj.send_data('reboot -f')
            time.sleep(60)
