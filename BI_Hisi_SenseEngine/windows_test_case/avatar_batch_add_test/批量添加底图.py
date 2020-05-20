#coding=utf-8
import time
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose

class test_BatchAdd(object):
    def __init__(self):
        '''批量添加图片测试'''
        # 引用方法类
        self.ScreenFile = Screenshots_operation("批量添加底图测试结果")
        self.operation = Autoit_Upper_machine_function()
        self.imgdis = images_dispose()
        self.windows_command = Command()
        self.path_img = self.ScreenFile.create_file("连续添加批量图片截图文件") + "\\"  # 创建图片存在的文件夹
        self.library_img = self.ScreenFile.create_file("连续添加后数量截图文件") + "\\"  # 创建图片存在的文件夹

    def batch_init(self):
        # 启动上位机并选择串口
        self.operation.init_start()
        # 删除所有图片
        self.operation.delete_all()

    def batch_add(self,firstname,name):#批量添加图片并且保存结果
        self.imgdis.rename(firstname)  # 更改每次图片名
        images = str(self.imgdis.images_str())  # 添加图片的名字集
        self.operation.batchAdd_img(images)  # 批量添加图片
        self.ScreenFile.window_capture(self.path_img + name)  # 截取当前添加结果图
        self.operation.click_addBatch_ok()
        path_one = str(self.path_img + 'SenseEngineCamera_Batch_%s.jpg' % 1)
        path_two = str(self.path_img + name)
        self.ScreenFile.compare_images(path_one, path_two)
        text = self.imgdis.get_img_text(path_two)  # 获取当前截图文字
        self.ScreenFile.log.logger.debug("--------%s-------" % text)

if __name__ == '__main__':
    batch = test_BatchAdd()
    error_number = 0
    successful_number=0
    text_max=2000

    #开始测试
    batch.ScreenFile.log.logger.debug("-----------test start------------")
    # 启动上位机并选择串口,删除所有图片,初始化
    batch.batch_init()
    # 开始测试
    for i in range(1,text_max+1):  # 循环次数
        batch.ScreenFile.log.logger.debug("-----------test: %s------------" % i)
        try:
            firstname = 'Test_threadNum_%s_' % i  # 定义本次添加图片名字头
            sceen_img_name ='SenseEngineCamera_Batch_%s.jpg' % i
            batch.batch_add(firstname,sceen_img_name)
            successful_number+=1
        except Exception as e:
            error_number += 1
            batch.ScreenFile.log.logger.debug("------------程序错误：%s------------%s"%(e,error_number))
            time.sleep(5)
            batch.windows_command.close_exe()
            time.sleep(2)
            batch.operation.init_start()
            time.sleep(1)
    batch.ScreenFile.log.logger.debug("--test finish: 成功:%s-出错：%s-------" % (successful_number,error_number))
