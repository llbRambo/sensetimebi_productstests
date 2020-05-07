import shutil,os,time,datetime,random
from psutil import disk_partitions
from subprocess import Popen, PIPE
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig

class Udisk_dispose(object):
    def __init__(self):
        '''
        U盘处理
        '''
        self.getConfig = datagetConfig()
        self.file_path = self.getConfig.getConfig().get("file_M20")  # 升级文件地址
        #self.file_path = self.getConfig.getConfig().get("file_M10")  # 升级文件地址

    def timeout_command(self,command, timeout=30):
        start = datetime.datetime.now()
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        print(command)
        while process.poll() is None:
            time.sleep(0.2)
            now = datetime.datetime.now()
            if (now - start).seconds > timeout:
                print("execute command timeout")
                process.kill()
                return None
        return process.stdout.read()

    def file_name(self,path):#文件获取
        filenames = []
        endswith = "\\DownloadImages"
        for files in os.listdir(path):
                file = os.path.join(path, files)
                filenames.append(file+endswith)
        print(filenames)
        return filenames

    def file_bin(self):#文件获取
        filenames = []
        endswith = "\\update_tar.bin"
        for files in os.listdir(self.file_path):
                file = os.path.join(self.file_path, files)
                filenames.append(file+endswith)
        #print(filenames)
        return filenames

    def chose_file(self):
        filenames = self.file_bin()
        lengths = len(filenames)
        if lengths == 1:
            filenames_path = filenames[0]
        elif lengths > 1:
            n = random.randint(0, lengths - 1)  # 随机版本号
            filenames_path = filenames[n]
        else:
            print("当前文件内没有版本")
        return filenames_path

    def removeSD(self,time_out=5 * 60, isCopyFile=False, src_path=''):
        wait_time = 0
        while True:

            time.sleep(2)
            #  遍历所有驱动器
            for item in disk_partitions():
                if 'removable' in item.opts:
                    driver = item.device
                    #print(driver)
                    if src_path != '':
                        if isCopyFile:
                            for l in os.listdir(src_path):
                                shutil.copyfile(src_path + "\\" + l, driver + "\\" + l)
                                time.sleep(1)
                                #print(l)
                            time.sleep(5)
                        print('发现usb驱动：%s, remove' % driver)
                    #timeout_command(getConfig().get("path_spti") + ' ' + driver.split(":")[0] + ":")
                    self.timeout_command(self.getConfig.getConfig().get("path_spti")+ ' ' + driver.split(":")[0] + ":")
                    return True
            wait_time += 2
            if wait_time > time_out:
                print("Timeout to wait SD card")
                return False
            print("wait ..")


if __name__ == '__main__':
    file_path = "D:\\test\\updata\\M20"#升级文件地址
    ud = Udisk_dispose()

    while True:
        udgrade_file=ud.chose_file(file_path)
        vension_file = udgrade_file.split("\\")
        print(vension_file[4])
