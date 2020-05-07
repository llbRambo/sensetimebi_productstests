#coding=utf-8
import time
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose
from BI_SenseEngine.ShareScripts.Udisk_dispose import Udisk_dispose



class Bin_upgrade(object):
    def __init__(self):
        # 准备数据

        getConfig = datagetConfig()
        self.star_times = getConfig.getConfig().get("star_times")  # 等待时长
        # 引用方法类
        self.ScreenFile = Screenshots_operation("Bin文件升级测试结果")
        self.udis = Udisk_dispose()
        self.operation = Autoit_Upper_machine_function()
        self.imgdis = images_dispose()
        self.windows_command = Command()
        # 创建图片文件夹
        self.vension_img = self.ScreenFile.create_file("Bin升级版本截图") + "\\"  # 创建图片存在的文件夹
        self.upload_img = self.ScreenFile.create_file("Bin升级上传文件截图")+"\\"
        self.open_img = self.ScreenFile.create_file("Bin升级打开视频流件截图")+"\\"

    def check_Upper_machine(self,name):
        '''
        查询当前版本确认上位机正常打开
        :param name:
        :return:
        '''
        flag = self.ScreenFile.screnn_vension(str(self.vension_img + name))  # 获取当前版本
        if flag is True:
            pass
        else:
            self.operation.click_close()  # 关闭上位机
            self.operation.init_start()  # 没有查询到版本重新打开上位机

    def bin_upgrade(self,screen_name):
        '''
        升级设备并且截图，等待设备启动
        :param screen_name:
        :return:
        '''
        udgrade_file = bindis.udis.chose_file()  # 选择当前上级文件
        vension_file = udgrade_file.split("\\")
        bindis.ScreenFile.log.logger.debug("----当前选择版本:%s----" % vension_file[4])
        self.ScreenFile.screen_upload(udgrade_file,self.upload_img+screen_name)#上传并且截图上传后图片
        time.sleep(self.star_times)  # 等待设备启动

    def start_eUpper_machine(self,open_name):
        '''
        启动上位机并且截图
        :param reboot_name:
        :return:
        '''
        self.operation.init_start()
        time.sleep(5)
        self.ScreenFile.window_capture(self.open_img+open_name)

if __name__ == '__main__':
    error_number = 0
    successful_number = 0
    text_max = 200000
    bindis = Bin_upgrade()
    bindis.ScreenFile.log.logger.debug("---------test_start------------")
    #查询当前版本确认上位机正常打开
    start_name ="vensin_start.jpg"
    cycle_name = "cycle_vension.jpg"  # 版本名字
    bindis.operation.init_start()  # 启动上位机
    bindis.check_Upper_machine(start_name)#查看当前版本
    bindis.operation.click_close()  # 关闭上位机
    for i in range(1,text_max+1):
        try:
            bindis.ScreenFile.log.logger.debug("-------------test:%s---------"%i)
            screen_name = "screen_upload_%s.jpg"%i
            open_name = "bin_open_%s.jpg"%i
            bindis.start_eUpper_machine(open_name)#启动上位机并且截图
            bindis.check_Upper_machine(cycle_name)# 查询当前版本确认上位机正常打开
            bindis.bin_upgrade(screen_name)  # #升级设备并且截图等待设备启动
        except Exception as e:
            error_number += 1
            bindis.ScreenFile.log.logger.debug("-------------test_error:%s-%s--------"%(e,error_number))
    bindis.ScreenFile.log.logger.debug("-------test finish -----------")

