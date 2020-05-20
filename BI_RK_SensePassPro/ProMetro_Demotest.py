# coding: utf-8
#
import uiautomator2 as u2
import time
import autoit
import os
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
        pm_list_cmd = 'adb -s ' + self.__AndroidDevice + ' shell pm uninstall ' + u_packagename
        info = os.popen(pm_list_cmd).read()
        print(info)
        flag = self.find_apk(u_packagename)
        if flag != -1:
            print('apk 卸载失败！！！')
            return True
        else:
            print('apk 卸载成功！！！')
            return False

    # def adb_

if __name__ == '__main__':
    ipport = '10.9.40.79:8888'
    packagename = 'com.sensetime.bi.powerondemo'
    for i in range(1,101):
        print('——————test：%s——————'%i)
        adb = AdbOpt(ipport)
        d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
        d.app_start(package_name="com.example.haerbinmetrodemo", activity="com.example.haerbinmetrodemo.MainActivity")
        time.sleep(3)

        # apk静默升级接口测试
        d(resourceId="com.example.haerbinmetrodemo:id/button").click()    #点击“确认升级apk”
        find_package = False
        while find_package == False:
            find_package = adb.find_apk(packagename)
            if find_package:
                print('apk 已经安装！！！！')
        time.sleep(5)
        adb.uninstall_apk(packagename)
        time.sleep(5)

        #Rom ota接口测试
        d(resourceId="com.example.haerbinmetrodemo:id/button2").click() # 点击“确认升级ROM” ，设备升级会重启，需要重新连接设备
        time.sleep(10)
        d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
        time.sleep(4*60)  #等待设备开机亮屏

        # 重启系统接口测试
        d.app_start(package_name="com.example.haerbinmetrodemo", activity="com.example.haerbinmetrodemo.MainActivity")
        time.sleep(2)
        d(resourceId="com.example.haerbinmetrodemo:id/button3").click()    #  点击“重启系统”按钮
        time.sleep(60)  #等待设备开机亮屏
