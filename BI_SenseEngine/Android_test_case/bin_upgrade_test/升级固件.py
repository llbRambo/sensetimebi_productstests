#-- coding: utf-8 --
from M20_Android.pages import Device_pro
from sensetimebi_productstests.BI_SenseEngine
import os
if __name__ == '__main__':
    ip = "10.9.40.22:8888"
    bin_name = 'm10_V3.2.1_update_tar.bin'
    # upgrade_need_time = 220 #Rom-V3.2.0升级所需时间
    upgrade_need_time = 255  #Rom-V3.2.1升级所需时间
    test_max = 1000
    D = Device_pro(ip, "升级固件")
    upload_fail_paths = D.create_file("升级固件失败截图") + "\\"
    start_path = D.create_file("升级后打开预览界面截图") + "\\"
    for i in range(1, test_max+1):
        while True:
            #现确认UVC节点已经挂载成功，在操作安卓上位机
            cmd_command_checkUvc = 'adb -s ' + ip + ' shell ls /dev -all'
            checkUvc_info = os.popen(cmd_command_checkUvc).read()
            #print(checkUvc_info)
            uvc_flag = checkUvc_info.find('ttyACM0')
            if uvc_flag != -1:
                print('Uvc 已经挂载成功！！！')
                D.start_app() #启动apk
                D.check_Report_switch()
                D.into_preview() #进入预览界面
                start_name = "start_%s.jpg"%i
                D.screen_img(start_path, start_name)
                upload_name = "upload_%s.jpg"%i
                # D.upgradetime(i, upload_fail_paths, upload_name, bin_name, upgrade_need_time)
                D.upgradetime(i, upload_fail_paths, upload_name, bin_name)
                break
            else:
                pass