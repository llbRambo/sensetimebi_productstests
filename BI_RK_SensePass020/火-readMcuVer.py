# coding: utf-8
#
import uiautomator2 as u2
import time
import autoit
if __name__ == '__main__':
    ipport = '10.9.40.106:8888'
    d = u2.connect_adb_wifi(ipport)  # 连接安卓设备

    uccess_count = 0
    fail_count = 0

    for i in range(1, 1000):
        print('——————————test%s——————————'%i)
        d.app_start(package_name="com.sensetime.sensepass.factoryexam", activity="com.sensetime.sensepass.factoryexam.MainActivity")
        time.sleep(3)
        d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_customized_args_verify").click()  # 点击定制数据检测
        time.sleep(10)  #等待mcu版本被读出来
        tv_receive_data = d.xpath('//*[@resource-id="com.sensetime.sensepass.factoryexam:id/tv_exec_cmd_result"]').get_text()
        print(tv_receive_data)
        flag = tv_receive_data.find('Mcu版本    ：  7')
        if flag != -1:
            print('测试成功')
            d(resourceId="com.sensetime.sensepass.factoryexam:id/iv_test_pass").click()  # da打勾
            time.sleep(2)
            uccess_count += 1
        else:
            print('测试失败')
            d(resourceId="com.sensetime.sensepass.factoryexam:id/iv_test_error").click() #打叉
            time.sleep(2)
            fail_count += 1
        d.app_clear("com.sensetime.sensepass.factoryexam") #杀掉apk
        print('测试成功累计次数：%s'%uccess_count)
        print('测试失败累计次数：%s'%fail_count)
        time.sleep(3)
