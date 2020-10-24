#-- coding: utf-8 --
from M20_Android.pages import Device_pro
from sensetimebi_productstests.BI_Hisi_SenseEngine.Android_test_case.AndroidShareScripts.pages import SenseEngineCameraDemoDebugApk
from sensetimebi_productstests.Sharedscript.File_operations import File_operations
from sensetimebi_productstests.Sharedscript.SharedAdbOperation import AdbOpt


if __name__ == '__main__':
    ip = "10.9.99.155:8888"

    # 先创建测试结果文件夹，里面存放log、截图等跟测试结果有关的文件
    result_files = File_operations()  # 实例化文件操作对象，用于测试结果相关文件的操作
    reboot_path = result_files.create_floder("单个添加用户",'D:\\test-project\\007-M10_M20\\scripts-test-result')  # 在当前路径下创建测试结果文件夹，用于存放测试结果相关文件

    test_max = 2000
    D = SenseEngineCameraDemoDebugApk(ip, reboot_path)
    # reboot_path =D.create_file("重启后打开预览界面截图")+"\\"
    D.start_app()
    # D.check_Report_switch()
    D.into_preview()
    for i in range(1,test_max+1):
        reboot_name = "reboot_%s.jpg"%i
        D.reboot_system(i,reboot_path,reboot_name)
