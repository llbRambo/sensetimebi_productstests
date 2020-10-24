# coding: utf-8

import uiautomator2 as u2
import string
import autoit

import os
import time

class AdbOpt(object):
    def __init__(self, AndroidDevice):
        self.__AndroidDevice = AndroidDevice
        os.popen('adb connect %s' % self.__AndroidDevice)
        os.popen('adb -s %s root ' % self.__AndroidDevice)
        os.popen('adb connect %s' % self.__AndroidDevice)
        os.popen('adb -s %s remount ' % self.__AndroidDevice)

    def find_package(self, f_packagename):
        info = os.popen('adb -s %s shell pm list packages'%self.__AndroidDevice).read()
        print(info)
        flag = info.find(f_packagename)
        if flag != -1:
            return True
        else:
            return False

    def find_apk(self, f_apkname):
        info = os.popen('adb -s %s shell ps '%self.__AndroidDevice).read()
        # print(info)
        flag1 = info.find(f_apkname)
        if flag1 != -1:
            return True #  找到返回True
        else:
            return False #  没找到返回False

    def uninstall_package(self, u_packagename):
        info = os.popen('adb -s %s shell pm uninstall %s'%(self.__AndroidDevice, u_packagename)).read()
        print(info)
        flag = self.find_package(u_packagename)
        if flag != -1:
            print('apk 卸载失败！！！')
            return True
        else:
            print('apk 卸载成功！！！')
            return False

    def adb_screencap(self, screenshotname, StoragePath):
        os.popen('adb -s %s shell screencap -p /sdcard/%s.png'%(self.__AndroidDevice, str(screenshotname)))    #开始截取屏幕图片
        time.sleep(2)
        os.popen('adb -s %s pull /sdcard/%s.png %s' % (self.__AndroidDevice, str(screenshotname), str(StoragePath)))   #把截取图片导到电脑指定文件夹里
        time.sleep(2)
        os.popen('adb -s %s shell rm -rf /sdcard/%s.png'%(self.__AndroidDevice, str(screenshotname)))  #图片导完之后，删除设备端图片，防止设备端空间不足
        time.sleep(2)

    def adb_rm_files(self, filesdir):
        os.popen('adb -s %s shell rm -rf %s'%(self.__AndroidDevice, str(filesdir)))
        time.sleep(2)

    def adb_exist(self):
        checkinfo = os.popen('adb devices').read()
        # print('checkinfo：%s' % checkinfo)
        target_adb = self.__AndroidDevice + '	device'
        # print('target adb：%s' % target_adb)
        flag = checkinfo.find(target_adb)
        # print('flag： %s' % flag)
        if flag != -1:
            # print('devices already connected')
            pass
        else:
            os.popen('adb connect %s' % self.__AndroidDevice)

    def adb_reboot(self):
        os.popen('adb -s %s reboot ' % self.__AndroidDevice)

def connects(host):
    # 检查服务器是否连接
    print('########正在检查网络是否连接########')
    flag1 = 1
    flag2 = 1
    flag3 = 1
    while flag1 != -1 or flag2 != -1 or flag3 != -1:
        ping_host = 'ping ' + host
        info = os.popen(ping_host).read()
        # print(info)
        target_str1 = '请求超时。'
        target_str2 = '无法访问目标主机。'
        target_str3 = '一般故障。'
        flag1 = info.find(target_str1)  # 检查PC是否与设备连接上
        flag2 = info.find(target_str2)  # 检查PC是否连接上网络
        flag3 = info.find(target_str3)  # 检查PC是否连接上网络
        # if flag1 != -1 or flag2 != -1 or flag3 != -1:
        #      print('        网络未连接，请连接网络        ')
    print('########网络连接成功########')

if __name__ == '__main__':
    ipport = '10.9.40.106:8888'
    for i in range(1, 6):
        connects('10.9.40.106')
        adb = AdbOpt(ipport)
        d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
        time1 = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        print('--------------------[%s]: test No.%s--------------------' % (time1, i))
        # print(time1)
        b = ''.join(c for c in time1 if c not in string.punctuation)
        # print(b)
        picname = str(i) + str("_") + b
        print(picname)

        while True:
            flag = adb.find_apk('com.sensetime.sensepassege')
            if flag == True:
                while True:
                    rxy_flag = d(text="热成像仪断开连接").exists(30)  # 150秒内
                    if rxy_flag:
                        print('热成像仪断开连接')
                    else:
                        print('热像仪连接成功！！！')
                        adb.adb_screencap(picname, 'D:\\test-project\\009-火神mini\\不出流')
                        adb.adb_reboot()
                        break
                break



