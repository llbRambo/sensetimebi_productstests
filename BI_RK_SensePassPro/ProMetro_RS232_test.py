# coding: utf-8
#
import uiautomator2 as u2
import time
import autoit
import os
if __name__ == '__main__':
    ipport = '10.9.40.79:8888'
    d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
    d.app_start(package_name="com.sensetime.sensepass.factoryexam", activity="com.sensetime.sensepass.factoryexam.MainActivity")
    time.sleep(3)
    uccess_count = 0
    fail_count = 0


    d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_pcba_exam").click()
    time.sleep(2)
    for i in range(1, 1001):
        print('——————————test%s——————————'%i)
        d.xpath('//*[@resource-id="com.sensetime.sensepass.factoryexam:id/lv_result"]/android.widget.LinearLayout[4]').click()
        time.sleep(2)
        d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_start_exam").click()  #点击开始测试
        time.sleep(3)
        #点击第三方串口工具的“发送”按钮
        # autoit.mouse_click(button='left', x=1875, y=777, clicks=1, speed=-1)
        # time.sleep(3)

        tv_receive_data = d.xpath('//*[@resource-id="com.sensetime.sensepass.factoryexam:id/tv_receive_data"]').get_text()
        print(tv_receive_data)
        flag = tv_receive_data.find('收到数据：0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31')
        if flag != -1:
            print('测试成功')
            d(resourceId="com.sensetime.sensepass.factoryexam:id/iv_test_pass").click()  # da打勾
            time.sleep(2)
            d(resourceId="com.android.systemui:id/back").click()  # 点击系统返回键
            time.sleep(2)
            uccess_count += 1
        else:
            print('测试失败')
            d(resourceId="com.sensetime.sensepass.factoryexam:id/iv_test_error").click() #打叉
            time.sleep(2)
            d(resourceId="com.android.systemui:id/back").click()  # 点击系统返回键
            fail_count += 1
        print('测试成功累计次数：%s'%uccess_count)
        print('测试失败累计次数：%s'%fail_count)
        time.sleep(2)
