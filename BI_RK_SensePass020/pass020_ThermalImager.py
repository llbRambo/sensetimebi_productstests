# coding: utf-8
#
import uiautomator2 as u2
import time
import autoit
import os
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
from sensetimebi_productstests.Sharedscript.SharedAdbOperation import AdbOpt

if __name__ == '__main__':
    ipport = '10.9.40.67:8888'
    adb = AdbOpt(ipport)
    relay = SingleRelay('com33', 9600)
    for i in range(1, 200):
        print('————————test:%s————————'%i)
        relay.disconnect_power()    # 给设备上电
        time.sleep(30)  # 等待设备开机
        d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
        d.app_start(package_name="com.sensetime.sensepass.factoryexam", activity="com.sensetime.sensepass.factoryexam.MainActivity")
        time.sleep(1)

        d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_hot_Phase_meter").click()  # 点击 热像仪测试
        time.sleep(1)
        d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_guide").click()  # 点击 高德
        time.sleep(1)
        d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_hot_ageing").click()  # 点击 老化测试
        time.sleep(5*60)
        adb.adb_screencap(i, 'D:\\test-project\\009-火神mini\\不出流')
        time.sleep(1)
        relay.connect_power()
        time.sleep(0.1)   #给设备下电
