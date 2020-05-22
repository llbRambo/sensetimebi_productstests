#-- coding: utf-8 --
from sensetimebi_productstests.BI_Hisi_SenseEngine.Android_test_case.AndroidShareScripts.pages import SenseEngineCameraDemoDebugApk
from sensetimebi_productstests.Sharedscript.File_operations import File_operations
import os
if __name__ == '__main__':
    ip = "10.9.40.74:8888"
    bin_name = 'm10_V3.2.2_update_tar.bin'
    test_max = 1000

    # 先创建测试结果文件夹，里面存放log、截图等跟测试结果有关的文件
    result_files = File_operations()  # 实例化文件操作对象，用于测试结果相关文件的操作
    path = result_files.create_floder("固件升级测试log")  # 在当前路径下创建测试结果文件夹，用于存放测试结果相关文件
    print(path)
    upload_fail_paths = result_files.create_floder('固件升级失败截图') # + "\\"
    print(upload_fail_paths)
    start_path = result_files.create_floder('升级后打开预览界面截图') # + "\\"
    print(start_path)

    D = SenseEngineCameraDemoDebugApk(ip, path)
    for i in range(1, test_max+1):
        while True:
            #先确认UVC节点已经挂载成功，在操作安卓上位机
            checkUvc_info = os.popen('adb -s %s shell ls /dev -all'%ip).read()
            #print(checkUvc_info)
            uvc_flag = checkUvc_info.find('ttyACM0')
            if uvc_flag != -1:
                print('Uvc 已经挂载成功！！！')
                D.start_app() #启动apk
                D.into_preview() #进入预览界面
                preview_interface_screenshot_name = "preview_%s.jpg" % i
                D.screen_img(start_path, preview_interface_screenshot_name)
                upgrade_interface_screenshot_name = "upgrade_%s.jpg" % i
                D.upgradetime(i, upload_fail_paths, upgrade_interface_screenshot_name, bin_name)
                break
            else:
                pass