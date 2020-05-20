#coding=utf-8
import time
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose

if __name__ == '__main__':


        '''批量添加图片测试'''
        # 准备数据
        error_number = 0
        successful_number=0
        text_max = 20000
        # 引用方法类
        ScreenFile = Screenshots_operation("单个添加底图测试结果")
        operation = Autoit_Upper_machine_function()
        imgdis = images_dispose()
        windows_command = Command()
        library_img = ScreenFile.create_file("单个添加后数量截图文件") + "\\"  # 创建图片存在的文件夹
        #开始测试
        ScreenFile.log.logger.debug("-----------test start------------")
        # 启动上位机并选择串口
        operation.init_start()
        #删除所有图片
        operation.delete_all()
        # 开始测试
        for i in range(1,text_max+1):
            try:
                ScreenFile.log.logger.debug("--------test: %s---------"%i)
                operation.add_img( "test_%s" % i)
            except Exception as e:
                error_number += 1
                ScreenFile.log.logger.debug("------------程序错误：%s------------%s" % (e, error_number))
        operation.get_library()
        ScreenFile.window_capture(library_img + 'library.jpg')  # 截取当前添加结果图
        ScreenFile.log.logger.debug("-------test finish -----------")


