#-- coding: utf-8 --
from sensetimebi_productstests.BI_Hisi_SenseEngine.Android_test_case.AndroidShareScripts.pages import SenseEngineCameraDemoDebugApk
from sensetimebi_productstests.Sharedscript.File_operations import File_operations
from sensetimebi_productstests.Sharedscript.SharedAdbOperation import AdbOpt

if __name__ == '__main__':
    ip = "10.9.66.29:8888"
    test_max = 10000

    # 先创建测试结果文件夹，里面存放log、截图等跟测试结果有关的文件
    result_files = File_operations()  # 实例化文件操作对象，用于测试结果相关文件的操作
    path = result_files.create_floder("单个添加特征值", 'D:\\test-project\\007-M10_M20\\scripts-test-result')  # 在当前路径下创建测试结果文件夹，用于存放测试结果相关文件

    D = SenseEngineCameraDemoDebugApk(ip, path)
    adb = AdbOpt(ip)

    D.start_app()
    D.into_preview()
    D.add_an_user("1")
    D.get_feature("1")
    for i in range(1, test_max+1):
        adb.adb_rm_files('/sdcard/Pictures/*.jpg')  # 删除在预览界面主动上报的图，防止占用内存
        D.add_feature(str(i))
        D.log.logger.debug("----------test_%s----------"%i)