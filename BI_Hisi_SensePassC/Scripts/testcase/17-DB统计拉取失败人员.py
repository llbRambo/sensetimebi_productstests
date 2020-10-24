#!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://www.jianshu.com/p/486dd9993125

import paramiko
from scp import SCPClient
import sqlite3
from prettytable import PrettyTable
import time
import os
import shutil


class SCP(object):
    def __init__(self, host, port, username, pass_wd, img_path, remote_path):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__pass_wd = pass_wd
        self.__local_path = img_path
        self.__remote_path = remote_path

        self.ssh = paramiko.SSHClient()

    def connects(self):
        # 连接服务器
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.__host, port=self.__port, username=self.__username, password=self.__pass_wd,
                         timeout=5)

    def download_file(self):
        _scp = SCPClient(self.ssh.get_transport(), socket_timeout=30.0)
        _scp.get(self.__remote_path, self.__local_path)
        print("info: " + self.__host + " download files successfully！")

    def download_img(self,log_file):
        _scp = SCPClient(self.ssh.get_transport(), socket_timeout=30.0)
        print("info: copying img......")

        try:
            file = open(log_file, 'r')
            while 1:
                line = file.readline().strip('\n')
                _scp.get(line, self.__local_path)
                if not line:
                    break
        except FileNotFoundError:
            print("file not exit!")

        print("info: finish copying")

    def disconnect(self):
        # 断开服务器
        self.ssh.close()

    def send_data(self, command):
        # 执行对应命令
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout

    @staticmethod
    def log_out():
        paramiko.util.log_to_file('/ssh_log')


class ConnSql(object):
    def __init__(self, file):
        self.__file = file
        self.sql_conn = sqlite3.connect(self.__file)
        print("info: read database successfully！")

    def execute_command(self, sql):
        cursor = self.sql_conn.cursor()
        cursor = cursor.execute(sql)
        return cursor

    @staticmethod
    def print_table(cursor):
        table = PrettyTable(['index', 'name', 'result', 'sync_status'])
        index = 1
        for row in cursor:
            table.add_row([index, str(row[2]), str(row[13]), str(row[-1])])
            index = index + 1
        print(table)

    @staticmethod
    def write_file(remote, cursor, log_file):
        with open(log_file, 'w') as file:
            for row in cursor:
                file.write(remote + str(row[13]) + ".jpg\n")

    def disconnect(self):
        self.sql_conn.close()


if __name__ == '__main__':
    host_ip = "192.168.1.103"
    use_port = 22
    login_name = "root"
    login_pwd = "123456"
    sql = "select * from users where sync_status == -1"
    current_path = os.path.dirname(__file__)
    remote_db_path = "/data/bi/application/db/linksync.db"
    local_db_path = current_path + "/linksync.db"
    remote_img_path = "/data/bi/application/usr_image/"
    log_file_path = current_path + '/sql_bug.txt'

    local_img_path = "img"
    if not os.path.isdir(local_img_path):
        os.mkdir(local_img_path)
    else:
        shutil.rmtree(local_img_path)
        os.mkdir(local_img_path)

    print("--------------- import image start ---------------")

    scp = SCP(host_ip, use_port, login_name, login_pwd, local_db_path, remote_db_path)
    scp.connects()
    scp.download_file()
    time.sleep(6)

    print local_db_path
    sql_conn = ConnSql(local_db_path)
    result = sql_conn.execute_command(sql)
    sql_conn.write_file(remote_img_path, result, log_file_path)
    sql_conn.print_table(result)
    sql_conn.disconnect()
    time.sleep(3)

    scp2 = SCP(host_ip, use_port, login_name, login_pwd, local_img_path, remote_img_path)
    scp2.connects()
    scp2.download_img(log_file_path)
