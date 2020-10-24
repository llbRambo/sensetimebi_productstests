#!/usr/bin
#coding=utf-8
import os
import time

class AdbOpt(object):
    def __init__(self, AndroidDevice):
        self.__AndroidDevice = AndroidDevice
        os.popen('adb connect %s' % self.__AndroidDevice)
        os.popen('adb -s %s root ' % self.__AndroidDevice)
        os.popen('adb connect %s' % self.__AndroidDevice)
        os.popen('adb -s %s remount ' % self.__AndroidDevice)

    def find_apk(self, f_packagename):
        info = os.popen('adb -s %s shell pm list packages'%self.__AndroidDevice).read()
        print(info)
        flag = info.find(f_packagename)
        if flag != -1:
            return True
        else:
            return False

    def uninstall_apk(self, u_packagename):
        info = os.popen('adb -s %s shell pm uninstall %s'%(self.__AndroidDevice, u_packagename)).read()
        print(info)
        flag = self.find_apk(u_packagename)
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

if __name__ == '__main__':
    ip = '10.9.40.33:8888'
    checkinfo = os.popen('adb devices').read()
    print('checkinfo：%s'%checkinfo)
    target_adb = ip + '	device'
    print('target adb：%s'%target_adb)
    flag = checkinfo.find(target_adb)
    print('flag： %s'%flag)
    if flag != -1:
        print('devices already connected')
        pass
    else:
        os.popen('adb connect %s'%ip)
