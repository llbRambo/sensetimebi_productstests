#!/usr/bin
#coding=utf-8
import os
import time

class AdbOpt(object):
    def __init__(self, AndroidDevice):
        self.__AndroidDevice = AndroidDevice


    def find_apk(self, f_packagename):
        pm_list_cmd = 'adb -s ' + self.__AndroidDevice + ' shell pm list packages'
        info = os.popen(pm_list_cmd).read()
        print(info)
        flag = info.find(f_packagename)
        if flag != -1:
            return True
        else:
            return False

    def uninstall_apk(self, u_packagename):
        pm_uninstall_cmd = 'adb -s ' + self.__AndroidDevice + ' shell pm uninstall ' + u_packagename
        info = os.popen(pm_uninstall_cmd).read()
        print(info)
        flag = self.find_apk(u_packagename)
        if flag != -1:
            print('apk 卸载失败！！！')
            return True
        else:
            print('apk 卸载成功！！！')
            return False

    def adb_screencap(self, screenshotname, Storagepath):
        screencap_cmd = 'adb -s ' + self.__AndroidDevice + ' shell  screencap -p /sdcard/' + str(screenshotname) + '.png'
        os.popen(screencap_cmd)  #开始截取屏幕图片
        time.sleep(2)
        adb_pull_cmd = 'adb -s ' + self.__AndroidDevice + ' pull /sdcard/' + str(screenshotname) + '.png  ' + str(Storagepath)
        os.popen(adb_pull_cmd)   #把截取图片导到电脑指定文件夹里
        time.sleep(2)
        adb_delete_screenshot_cmd = 'adb -s ' + self.__AndroidDevice + ' shell rm -rf /sdcard/' + str(screenshotname) + '.png  '
        os.popen(adb_delete_screenshot_cmd)  #图片导完之后，删除设备端图片，防止设备端空间不足
        time.sleep(2)



