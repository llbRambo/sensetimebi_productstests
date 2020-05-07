#coding=utf-8
import time
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.service_serial import M20_serial

class test_reboot(object):
    def __init__(self):
        '''reboot测试'''
        # 准备数据
        getConfig = datagetConfig()
        equipment_port = getConfig.getConfig().get("equipment_port")#获取设备串口号
        self.star_times = getConfig.getConfig().get("star_times")#重启等待时长
        #引用公共类
        self.equipment_ser = M20_serial(port=equipment_port, baudrate = 115200)
        self.operation = Autoit_Upper_machine_function()
        self.windows_command = Command()
        self.ScreenFile = Screenshots_operation("软重启测试结果")
        # 创建图片文件夹
        self.reboot_img = self.ScreenFile.create_file("M20软重启后识别图") + "\\"  # 创建图片存在的文件夹

    def reboot_equipment(self):
        '''
        重启并关闭上位机
        :return:
        '''
        #处理reboot传输
        reboot = self.equipment_ser.asc_str("reboot")
        #print(reboot)
        enter = self.equipment_ser.asc_str("")
        time.sleep(0.02)
        self.equipment_ser.send_cmd(enter)
        self.equipment_ser.send_cmd(reboot)
        time.sleep(self.star_times)

    def start_eUpper_machine(self,reboot_name):
        '''
        启动上位机并且截图后关闭上位机
        :param reboot_name:
        :return:
        '''
        self.operation.init_start()
        time.sleep(3)
        self.ScreenFile.window_capture(self.reboot_img+reboot_name)
        self.operation.click_close()

if __name__ == '__main__':

        test_max = 5000
        reboot_dis = test_reboot()
        reboot_dis.ScreenFile.log.logger.debug("----------test start---------")
        for i in range(1,test_max+1):
            reboot_dis.ScreenFile.log.logger.debug("----------test:   %s---------"%i)
            try:
                reboot_name = "reboot_%s.jpg"%i
                reboot_dis.reboot_equipment()#发送重启命令
                reboot_dis.start_eUpper_machine(reboot_name)#打开上位机检查重启并且截图
            except Exception as e:
                reboot_dis.windows_command.close_exe()#关闭上位机
                reboot_dis.ScreenFile.log.logger.debug("----------test:   %s-------fail" % e)
