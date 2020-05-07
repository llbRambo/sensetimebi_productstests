import time,os
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig

class Command(object):
    def __init__(self):

        getConfig = datagetConfig()
        self.closecommand = getConfig.getConfig().get("closecommand")  # 关闭上位机命令
        self.Process_name = getConfig.getConfig().get("Process_name")#上位机进程名
        self.pc_exe_path = getConfig.getConfig().get("pc_exe_path")  # 上位机路径


    def start_exe(self, command):
        os.popen(command)
        time.sleep(2)

    def close_exe(self):
        os.system(self.closecommand)
        time.sleep(0.02)

    def check_exe(self, startcommand='tasklist'):
        mytasklist = os.popen(startcommand)
        time.sleep(2)
        mytasklists = mytasklist.read()  # 读取输出
        return mytasklists

    def check_close_exe(self):
        mytasklists = self.check_exe()
        if mytasklists.find(self.Process_name) != -1:
            self.close_exe()
        else:
            print('播放器已经关闭')
        time.sleep(1)

    def check_start_exe(self):

        mytasklists = self.check_exe()
        if mytasklists.find(self.Process_name) != -1:
            print('播放器已经打开')
        else:
            self.start_exe(self.pc_exe_path)
        time.sleep(1)

if __name__ == '__main__':
    Process_name = 'SenseEngineCameraV1.0.9.e'
    pc_exe_path = 'D:\Tools\\PC上位机\\SenseEngineCameraV1.0.9\\SenseEngineCameraV1.0.9.exe'
    windowsCommand = Command()
    for i in range(5):
        windowsCommand.check_close_exe()