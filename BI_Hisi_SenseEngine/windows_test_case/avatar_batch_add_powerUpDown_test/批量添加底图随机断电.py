#coding=utf-8
import time
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose
from BI_SenseEngine.ShareScripts.service_serial import M20_serial

class test_BatchAdd_power(object):
    def __init__(self):
        '''批量添加图片测试'''
        # 准备数据
        getConfig = datagetConfig()
        power_port = getConfig.getConfig().get("relay_port")#获取继电器串口号
        self.star_times = getConfig.getConfig().get("star_times")#重启等待时长
        # 引用方法类
        self.power_ser = M20_serial(port=power_port,baudrate =9600)
        self.ScreenFile = Screenshots_operation("批量添加底图测试结果")
        self.operation = Autoit_Upper_machine_function()
        self.imgdis = images_dispose()
        self.windows_command = Command()
        self.batch_power_img = self.ScreenFile.create_file("添加底图断电后重启截图文件") + "\\"  # 创建图片存在的文件夹

    def batch_init(self):
        # 启动上位机并选择串口
        self.operation.init_start()
        # 删除所有图片
        self.operation.delete_all()

    def batch_add(self,firstname):#批量添加图片
        self.imgdis.rename(firstname)  # 更改每次图片名
        images = str(self.imgdis.images_str())  # 添加图片的名字集
        self.operation.batchAdd_power(images)  # 批量添加图片

    def power_batch(self):#上下电关闭上位机并等待设备启动
        self.power_ser.power_operation()
        self.windows_command.close_exe()
        time.sleep(self.power_ser.switch_time())

    def start_eUpper_machine(self,power_name):
        '''
        启动上位机并且截图
        :param reboot_name:
        :return:
        '''
        self.operation.init_start()
        time.sleep(3)
        self.ScreenFile.window_capture(self.batch_power_img+power_name)


if __name__ == '__main__':
    Bpowers = test_BatchAdd_power()
    error_number = 0
    successful_number=0
    text_max=2000

    #开始测试
    Bpowers.ScreenFile.log.logger.debug("-----------test start------------")
    # 启动上位机并选择串口,删除所有图片,初始化
    Bpowers.batch_init()
    # 开始测试
    for i in range(1,text_max+1):  # 循环次数
        Bpowers.ScreenFile.log.logger.debug("-----------test: %s------------" % i)
        try:
            firstname = 'Test_threadNum_%s_' % i  # 定义本次添加图片名字头
            sceen_img_name ='batch_power_%s.jpg' % i
            Bpowers.batch_add(firstname)#批量添加图片
            Bpowers.power_batch()#上下电关闭上位机等待设备启动
            Bpowers.start_eUpper_machine(sceen_img_name)#启动上位机并且截图
            successful_number+=1
        except Exception as e:
            error_number += 1
            Bpowers.ScreenFile.log.logger.debug("------------程序错误：%s------------%s"%(e,error_number))
            time.sleep(5)
            Bpowers.windows_command.close_exe()
            time.sleep(2)
            Bpowers.operation.init_start()
            time.sleep(1)
    Bpowers.ScreenFile.log.logger.debug("--test finish: 成功:%s-出错：%s-------" % (successful_number,error_number))
