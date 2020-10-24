import os
import sys
import re
import time
import paramiko
from scp import SCPClient

class SSH(object):
    # 初始化参数
    def __init__(self, host, port, username, passwd):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__passwd = passwd
        self.__stdin = ''
        self.__stdout = ''
        self.__stderr = ''
        self.ssh_client = paramiko.SSHClient()

    def connects(self):
        # 检查服务器是否连接
        print('########正在检查网络是否连接########')
        flag1 = 1
        flag2 = 1
        flag3 = 1
        while flag1 != -1 or flag2 != -1 or flag3 != -1:
            ping_host = 'ping ' + self.__host
            info = os.popen(ping_host).read()
            #print(info)
            target_str1 = '请求超时。'
            target_str2 = '无法访问目标主机。'
            target_str3 = '一般故障。'
            flag1 = info.find(target_str1)  #检查PC是否与设备连接上
            flag2 = info.find(target_str2)  #检查PC是否连接上网络
            flag3 = info.find(target_str3)  #检查PC是否连接上网络
            if flag1 != -1 or flag2 != -1 or flag3 != -1:
                print('        网络未连接，请连接网络        ')
        print('########网络连接成功########')

        #SSH连接设备
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname = self.__host,
                                    port = self.__port,
                                    username = self.__username,
                                    password = self.__passwd,
                                    timeout = 5)

    def disconnect(self):
        # 断开服务器
        self.ssh_client.close()


    def send_data(self, command):
        # 执行对应命令
        #print('command: %s'%command)
        # stdin, stdout, stderr = self.ssh_client.exec_command(command)  #bufsize=1024,,  timeout=70
        # return stdout.read().decode('utf-8')

        self.__stdin, self.__stdout, self.__stderr = self.ssh_client.exec_command(command)
        time.sleep(3)

    def get_data(self):
        return self.__stdout.read().decode('utf-8')


    def send_and_recv(self, command):
        shell = self.ssh_client.invoke_shell()
        shell.sendall(command)
        while 1:
            info = shell.recv(2048)
            print('info: ', info)



    # def send_data(self, command):
    #     # 执行对应命令
    #     stdin, stdout, stderr = self.ssh_client.exec_command(command)
    #     print('指令执行结果： ', stdout.read(1024).decode('utf-8'))
    #     return stdout

    def read_data(self):
        # 读取命令反馈信息
        return stdout.read().decode('utf-8')

class SCP(SSH):
    def __init__(self, host, port, username, passwd):
        SSH.__init__(self, host, port, username, passwd)

    # 把本地某个指定文件上传到远程主机指定路径
    def singleFile_upload(self, filename, local_path, remote_path):
        self.connects()
        _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
        local_file = str(local_path) + '\\' + str(filename)
        remote_path = str(remote_path)
        _scp.put(local_file, remote_path)
        print("file " + str(local_file) + " to " + str(remote_path) + "  upload  successfully.")
        self.disconnect()

    # 把远程主机上的文件传送到本地
    def singFile_download(self, filename, remote_path, local_path):
        self.connects()
        _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
        remote_file = str(remote_path) + '/' + str(filename)
        _scp.get(remote_file, local_path)
        print("file " + str(remote_file) + " to " + str(local_path) + "  download  successfully.")
        rmfile = 'rm -rf ' + remote_file  # 文件传送到本地之后，删除远程主机上的该文件
        self.send_data(rmfile)
        self.disconnect()

    # # 把本地某个指定路径下的所有文件上传到远程主机指定路径
    # def Files_upload(self, local_path, remote_path):
    #     self.connects()
    #     _scp = SCPClient(self.ssh_client.get_transport(), socket_timeout=30.0)
    #     _scp.put(local_path, remote_path)
    #     print("info:  upload files successfully！")
    #     self.disconnect()

    def modify_path(self, remote_path, local_path):
        self.__remote_path = remote_path
        self.__local_path = local_path


def chooseProject():
    while True:
        print('***************************************************************')
        print('1.SensePass X  2.SensePass C')
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
    # cur_path = sys.path[0]
    # 绝对路径
    cur_path = os.path.dirname(sys.argv[0])
    print(cur_path)
    scp_obj.singFile_download(filename, '/data/', cur_path)

def changeumode(ssh_obj):
    print('是否切换到工厂模式？')
    umodeFlag = input('yes或者no：').strip()
    if umodeFlag == 'yes':
        ssh_obj.send_data('params_rw umode 0')
        ssh_obj.send_data('reboot -f')
        print('设备正在切换到工厂模式，请耐心等待！！！')





def judge_legal_ip(one_str):
    '''
    正则匹配方法
    判断一个字符串是否是合法IP地址
    '''
    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(one_str):
        return True
    else:
        return False

if __name__ == '__main__':
    host_ip = ''
    isipflag = False
    while not isipflag:
        host_ip = input('请输入IP地址：').strip()
        isipflag = judge_legal_ip(host_ip)
        if not isipflag:
            print('输入错误，请输入IP地址！！！')

    print(host_ip)
    ssh_port = 22
    ssh_name = 'root'
    ssh_pwd = chooseProject()
    # print(ssh_pwd)

    ssh_obj = SSH(host_ip,ssh_port,ssh_name,ssh_pwd)
    scp_obj = SCP(host_ip, ssh_port, ssh_name, ssh_pwd)
    ssh_obj.connects()
    recordInfo(ssh_obj, scp_obj)
    changeumode(ssh_obj)
    os.system('pause')  # 按任意键退出

