#-- coding: utf-8 --
from sensetimebi_productstests.BI_Hisi_SenseEngine.Android_test_case.AndroidShareScripts.pages import SenseEngineCameraDemoDebugApk
from sensetimebi_productstests.Sharedscript.File_operations import File_operations
from sensetimebi_productstests.Sharedscript.SharedAdbOperation import AdbOpt
import os, time
if __name__ == '__main__':
    ip = "10.9.66.28:8888"
    bin_name = 'm20_V2.5.0_update_tar.bin'
    test_max = 250
    uvc_flag1 = True

    # 先创建测试结果文件夹，里面存放log、截图等跟测试结果有关的文件
    result_files = File_operations()  # 实例化文件操作对象，用于测试结果相关文件的操作
    path = result_files.create_floder("固件升级测试log", 'D:\\test-project\\007-M10_M20\\scripts-test-result')  # 在当前路径下创建测试结果文件夹，用于存放测试结果相关文件
    print(path)
    upload_fail_paths = result_files.create_floder('固件升级失败截图', 'D:\\test-project\\007-M10_M20\\scripts-test-result') # + "\\"
    print(upload_fail_paths)
    start_path = result_files.create_floder('升级后打开预览界面截图', 'D:\\test-project\\007-M10_M20\\scripts-test-result') # + "\\"
    print(start_path)

    D = SenseEngineCameraDemoDebugApk(ip, path)
    adb = AdbOpt(ip)
    for i in range(139, test_max+1):
        adb.adb_rm_files('/sdcard/Pictures/*.jpg')  # 删除在预览界面主动上报的图，防止占用内存
        uvc_load_starttime = time.time()
        while uvc_flag1:
            adb.adb_exist()  # 检测adb是否连接
            uvc_flag_list = ['ttyACM0', 'ttyACM1', 'ttyACM2']
            #先确认UVC节点已经挂载成功，在操作安卓上位机
            checkUvc_info = os.popen('adb -s %s shell ls /dev -all'%ip).read()
            #print(checkUvc_info)
            for a in uvc_flag_list:
                uvc_flag = checkUvc_info.find(a)
                if uvc_flag != -1:
                    uvc_load_endtime = time.time()
                    print('Uvc 已经挂载成功！！！')
                    uvc_flag1 = False
                    break
                else:
                    pass
                    # print('Uvc 正在挂载！！！')
        uvc_load_needtime = uvc_load_endtime - uvc_load_starttime
        print('uvc挂载时间为：%s'%uvc_load_needtime)

        D.start_app()  # 启动apk
        D.into_preview()  # 进入预览界面
        preview_interface_screenshot_name = "preview_%s.jpg" % i
        D.screen_img(start_path, preview_interface_screenshot_name)
        upgrade_interface_screenshot_name = "upgrade_%s.jpg" % i
        D.upgradetime(i, upload_fail_paths, upgrade_interface_screenshot_name, bin_name)

        os.popen('adb -s %s shell rm /dev/*ACM*'%ip)  # 释放uvc结点，防止影响的下次测试
        uvc_flag1 = True