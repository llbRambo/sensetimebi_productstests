#coding=utf-8
from interval import Interval
import paramiko
import time
from sensetimebi_productstests.Sharedscript.ShareedSSH import SSH

class hisi_ssh(object):
    # 初始化参数
    def __init__(self, host, port, username, passwd):
        self.__host = host
        self.__port = 22
        self.__username = username
        self.__passwd = passwd


    def connects(self):
        # 连接服务器
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = self.__host, port = self.__port, username = self.__username, password = self.__passwd)


    def disconnect(self):
        # 断开服务器
        self.ssh.close()
        

    def senddata(self, data):
        # 执行对应命令
        stdin, stdout, stderr = self.ssh.exec_command(data)
        return stdout


def get_proc_infor(iput_list):
    output_list = "".join(iput_list).split()
    proc_id = output_list[0]
    proc_vsz = output_list[4]
    proc_vsz_percent = output_list[5]
    proc_cpu_percent = output_list[6]
    proc_name = output_list[7]
    return proc_id, proc_name, proc_vsz, proc_vsz_percent, proc_cpu_percent


def judge_result(base, flux, pro_cpu):
    base = float(base.strip('%')) / 100
    pro_cpu = float(pro_cpu.strip('%')) / 100
    #flux = float(flux.strip('%')) / 100
    
    zoom_min = base - flux if base - flux >= 0 else 0
    zoom_max = base + flux if base + flux <= 1 else 1
    zoom_base_flux = Interval(zoom_min, zoom_max)
    if pro_cpu in zoom_base_flux:
        return "Pass"
    else:
        return "Fail"



if __name__ == '__main__':

    host_ip = "10.9.40.243"
    port = 22
    login_name = "root"
    login_pwd = "BI_SensePassXS#"
    #login_pwd = "123456"
    
    test_max = 500000
    delay_time = 20

    #配置需要监控的服务进程名称填写列表中
    service_list = ["device_service", "media_service", "camera_service", "sensor_service","cmd_service","ai_service", "fota_service", "sensepassx-app"]
    #service_list = ["media_service"]
    #service_list = ["sensepassx-app","media_service"]

    #配置虚拟内存允许的动态范围
    cpu_normal_range = 0.15

    print("---------------------------------------- System Test-zhujq -----------------------------------------")
    ss = SSH(host_ip, port, login_name, login_pwd)
    ss.connects()

    #保存每个服务进程的开始时的虚拟内存占有率
    init_proc_cpu_value = [0]*len(service_list)
    for i in range(0, len(service_list)):
        system_process_name = "top -n 1 |grep " +  service_list[i] + "|awk NR==1"
        proc_id, proc_name, real_time_proc_vsz, real_time_proc_vsz_percent, real_time_proc_cpu_percent = get_proc_infor(ss.send_data(system_process_name).readlines())
        init_proc_cpu_value[i] = real_time_proc_vsz_percent
        

    #检查系统进程的cpu占有率是否超过初始虚拟内存的预设范围  
    for loop_start in range(1,test_max+1):
        print("PID\t", "PID-NAME\t\t",  "PID-VSZ\t\t", "%VSZ\t\t", "%CPU\t\t",  "Result")
        for i in range(0, len(service_list)):
            system_process_name = "top -n 1 |grep " +  service_list[i] + "|awk NR==1"
            proc_id, proc_name, real_time_proc_vsz, real_time_proc_vsz_percent, real_time_proc_cpu_percent = get_proc_infor(ss.send_data(system_process_name).readlines())
            result = judge_result(init_proc_cpu_value[i], cpu_normal_range, real_time_proc_vsz_percent)
            print(proc_id, "\t", proc_name, "\t\t", real_time_proc_vsz, "\t\t", real_time_proc_vsz_percent, "\t\t",  real_time_proc_cpu_percent, "\t\t", result)
        time.sleep(delay_time)
        print("----------------------------------------------------------------------------------------------------------", loop_start)

    ss.disconnect()


