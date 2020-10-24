#-- coding: utf-8 --
import uiautomator2 as u2
import time
import os

def adb_screencap(ip, screenshotname, StoragePath):
    os.popen('adb -s %s shell screencap -p /sdcard/%s.png'%(ip, str(screenshotname)))    #开始截取屏幕图片
    time.sleep(2)
    os.popen('adb -s %s pull /sdcard/%s.png %s' % (ip, str(screenshotname), str(StoragePath)))   #把截取图片导到电脑指定文件夹里
    time.sleep(2)
    os.popen('adb -s %s shell rm -rf /sdcard/%s.png'%(ip, str(screenshotname)))  #图片导完之后，删除设备端图片，防止设备端空间不足
    time.sleep(2)


if __name__ == '__main__':
    ip = '10.9.66.64:8888'
    d = u2.connect_adb_wifi(ip)
    adb_screencap(ip, 0, 'D:\\test-project\\009-火神mini\\2')
    for i in range(1, 1001):
        testTime = time.strftime("%y%m%d_%H%M%S")
        print('——————[%s]:test %s——————'%(testTime, i))

        flag = False
        while not flag:
            d.long_click(0.422, 0.435, 5.0)
            flag = d(resourceId="com.sensetime.sensepassege:id/et_pwd").exists()
            print(flag)
            time.sleep(2)
        d(resourceId="com.sensetime.sensepassege:id/et_pwd").set_text("admin1234", timeout=5)
        time.sleep(2)
        d(resourceId="com.sensetime.sensepassege:id/tv_confirm").click()
        d(resourceId="com.sensetime.sensepassege:id/system_setting").click()

        d.xpath('//*[@resource-id="com.sensetime.sensepassege:id/temperature_detection"]/android.widget.RelativeLayout[1]/android.widget.Switch[1]').click()
        d(resourceId="com.sensetime.sensepassege:id/ib_left").click()
        d(resourceId="com.sensetime.sensepassege:id/ib_left").click()
        time.sleep(3)
        #截图
        adb_screencap(ip, i, 'D:\\test-project\\009-火神mini\\2')

        time.sleep(3)