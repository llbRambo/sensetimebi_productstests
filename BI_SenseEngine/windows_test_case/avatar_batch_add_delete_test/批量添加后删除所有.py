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
    text_max=2000

    # 引用方法类
    ScreenFile = Screenshots_operation("删除所有底图测试结果")
    operation = Autoit_Upper_machine_function()
    imgdis = images_dispose()
    windows_command = Command()
    #开始测试
    ScreenFile.log.logger.debug("-----------test start------------")
    # 启动上位机并选择串口
    operation.init_start()
    #删除所有图片
    operation.delete_all()
    # 开始测试
    for i in range(1,text_max+1):  # 循环次数
        try:
            ScreenFile.log.logger.debug("-----------test: %s------------"%i)
            firstname = 'Test_threadNum_%s_' % i  # 定义本次添加图片名字头
            imgdis.rename(firstname)  #更改每次图片名
            images = str(imgdis.images_str())  # 添加图片的名字集
            operation.batchAdd_img(images) #批量添加图片
            operation.click_addBatch_ok()
            operation.delete_all()
            successful_number+=1
        except Exception as e:
            error_number += 1
            ScreenFile.log.logger.debug("------------程序错误：%s------------%s"%(e,error_number))
            time.sleep(5)
            windows_command.close_exe()
            time.sleep(2)
            operation.init_start()
            time.sleep(1)
    ScreenFile.log.logger.debug("--test finish: 成功:%s-出错：%s-------" % (successful_number,error_number))
