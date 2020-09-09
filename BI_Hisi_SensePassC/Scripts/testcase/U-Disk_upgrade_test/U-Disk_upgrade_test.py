#!/usr/bin/python
#coding=utf-8
import sys, time
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH
from sensetimebi_productstests.Sharedscript.logger import Logger

if __name__ == '__main__':

    host_ip = '10.9.40.150'
    # print(host_ip)
    ssh_name = 'root'
    ssh_pwd = 'BI_SensePassXS#'
    # print(ssh_pwd)
    ssh_port = 22

    logpath = sys.path[0] + '\\log.txt'
    log = Logger(logpath, level='debug')  # 保存脚本运行log

    ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
    ssh_obj.connects()

    for i in range(1, 16):
        log.logger.debug('----------test No.%s----------' % i)
        ssh_obj.send_data("sed -i \"1i U disk upgrade\" /etc/product_info")
        ssh_obj.send_data("cat /etc/product_info")
        info = ssh_obj.get_data()
        log.logger.debug(info)
        flag = info.find('U disk upgrade')
        # print(flag)
        if flag != -1:
            log.logger.debug('flag set up success!!!')
        else:
            log.logger.debug('flag set up fail!!!')

        ssh_obj.send_data("reboot -f")
        log.logger.debug('waiting upgrade...')
        time.sleep(100)
        ssh_obj = SSH(host_ip, ssh_port, ssh_name, ssh_pwd)
        ssh_obj.connects()

        ssh_obj.send_data("cat /etc/product_info")
        info = ssh_obj.get_data()
        log.logger.debug(info)
        flag = info.find('U disk upgrade')
        if flag == -1:
            log.logger.debug('U disk upgrade success!!!')
        else:
            log.logger.debug('U disk upgrade fail!!!')






