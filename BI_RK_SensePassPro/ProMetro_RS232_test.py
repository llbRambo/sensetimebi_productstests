# coding: utf-8
#
import uiautomator2 as u2
import time
import autoit
import os
from sensetimebi_productstests.Sharedscript.logger import Logger

if __name__ == '__main__':
    ipport = '10.9.66.151:8888'
    log = Logger('D:\\test-project\\000-testScripts\\sensetimebi_productstests\\BI_RK_SensePassPro\\rs232.txt', level='debug')  #保存脚本运行log
    d = u2.connect_adb_wifi(ipport)  # 连接安卓设备
    #d.app_start(package_name="com.sensetime.sensepass.factoryexam", activity="com.sensetime.sensepass.factoryexam.MainActivity") #SelectDevActivity
    d.app_start(package_name="com.sensetime.sensepass.factoryexam",activity="com.sensetime.sensepass.factoryexam.SelectDevActivity")
    time.sleep(3)
    uccess_count = 0
    fail_count = 0

    d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_dev_pass").click()
    # d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_pcba_exam").click()
    d(resourceId="com.sensetime.sensepass.factoryexam:id/btn_pcba_exam").click()
    time.sleep(2)
    for i in range(1, 10001):
        log.logger.debug('——————————test%s——————————'%i)
        d.xpath('//*[@resource-id="com.sensetime.sensepass.factoryexam:id/lv_result"]/android.widget.LinearLayout[4]').click()
        time.sleep(3)
        #点击第三方串口工具的“发送”按钮
        # autoit.mouse_click(button='left', x=1875, y=777, clicks=1, speed=-1)
        # time.sleep(3)

        tv_receive_data = d.xpath('//*[@resource-id="com.sensetime.sensepass.factoryexam:id/tv_tips"]').get_text()
        # log.logger.debug(tv_receive_data)
        flag = tv_receive_data.find('4.RS232测试成功')
        if flag != -1:
            log.logger.debug('测试成功')
            time.sleep(5)
            d(resourceId="com.android.systemui:id/back").click()  # 点击系统返回键
            time.sleep(2)
            uccess_count += 1
        else:
            log.logger.debug('测试失败')
            d(resourceId="com.sensetime.sensepass.factoryexam:id/iv_test_error").click() #打叉
            time.sleep(2)
            d(resourceId="com.android.systemui:id/back").click()  # 点击系统返回键
            fail_count += 1
        log.logger.debug('测试成功累计次数：%s'%uccess_count)
        log.logger.debug('测试失败累计次数：%s'%fail_count)
        time.sleep(2)
