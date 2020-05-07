from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose
from BI_SenseEngine.ShareScripts.service_serial import M20_serial
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
import time


class operation_Camera(object):
    def __init__(self):
        # 准备数据
        getConfig = datagetConfig()
        open_rgb = getConfig.getConfig().get("open_rgb")
        open_ir = getConfig.getConfig().get("open_ir")
        close_rgb = getConfig.getConfig().get("close_rgb")
        close_ir = getConfig.getConfig().get("close_ir")
        ai_stop = getConfig.getConfig().get("stop_reo")  # 打开算法
        ai_start = getConfig.getConfig().get("start_reo")  # 关闭算法
        eqt_port = getConfig.getConfig().get("equipment_port")  # 获取设备串口号

        # 引用公共方法
        self.imgdis = images_dispose()
        self.ScreenFile = Screenshots_operation("打开关闭Camera测试结果")
        self.equipment_port = M20_serial(port=eqt_port, baudrate=115200)
        self.operation = Autoit_Upper_machine_function()
        self.windows_command = Command()

        # 处理命令ai
        self.open_Rgb = self.equipment_port.asc_str(open_rgb)
        self.open_Ir = self.equipment_port.asc_str(open_ir)
        self.close_Rgb = self.equipment_port.asc_str(close_rgb)
        self.close_Ir = self.equipment_port.asc_str(close_ir)
        self.stop_ai = self.equipment_port.asc_str(ai_stop)
        self.start_ai = self.equipment_port.asc_str(ai_start)

        # 创建图片存放地址
        self.open_img = self.ScreenFile.create_file('打开摄像头测试结果图片') + "\\"
        self.close_img = self.ScreenFile.create_file('关闭摄像头测试结果图片') + "\\"


    def close_camera(self):
        '''
        关闭摄像头
        :return:
        '''
        self.equipment_port.send_cmd(self.close_Rgb)
        self.equipment_port.send_cmd(self.close_Ir)
        self.equipment_port.send_cmd(self.stop_ai)
        time.sleep(10)

    def opne_camera(self):
        '''
        打开摄像头
        '''
        self.equipment_port.send_cmd(self.open_Rgb)
        self.equipment_port.send_cmd(self.open_Ir)
        self.equipment_port.send_cmd(self.start_ai)
        time.sleep(5)

    def close_machine(self):
        self.operation.click_close()
        self.windows_command.check_close_exe()

    def screen_close_ir_rgb(self,close_rgb_name,close_ir_name):
        self.operation.init_start()
        time.sleep(5)
        self.ScreenFile.window_capture(self.close_img+close_rgb_name)#RGB截图
        time.sleep(2)
        self.operation.switch_ir()
        time.sleep(1)
        self.close_machine()
        self.operation.init_start()
        time.sleep(6)
        self.ScreenFile.window_capture(self.close_img +close_ir_name)#ir截图
        time.sleep(1)
        self.operation.switch_rgb()

    def screen_open_ir_rgb(self,open_rgb_name,open_ir_name):
        '''
        打开摄像头截图
        :param open_rgb_name:
        :param open_ir_name:
        :return:
        '''
        # 打开摄像头
        self.operation.init_start()
        time.sleep(5)
        self.ScreenFile.window_capture(self.open_img+open_rgb_name)#RGB截图
        time.sleep(2)
        self.operation.switch_ir()
        time.sleep(1)
        self.ScreenFile.window_capture(self.open_img +open_ir_name)#ir截图
        time.sleep(1)
        self.operation.switch_rgb()


if __name__ == '__main__':
    test_max = 10000
    dis_camera = operation_Camera()
    dis_camera.ScreenFile.log.logger.debug("-----------test start----------")
    #开始测试
    for i in range(1,test_max+1):
        try:
            dis_camera.ScreenFile.log.logger.debug("-----------test: %s----------"%i)
            #截图命名
            close_rgb_name = 'close_rgb_%s.jpg'%i
            close_ir_name = 'close_ir_%s.jpg'%i
            open_rgb_name = 'open_rgb_%s.jpg'%i
            open_ir_name =  'open_ir_%s.jpg'%i

            #关闭摄像头
            dis_camera.ScreenFile.log.logger.debug("-----------test close :%s----------" % i)
            dis_camera.close_camera()#发送命令关闭摄像头
            dis_camera.screen_close_ir_rgb(close_rgb_name,close_ir_name)#截图关闭摄像头后的IR和RGB图
            dis_camera.close_machine()#关闭上位机

            #打开摄像头
            dis_camera.ScreenFile.log.logger.debug("-----------test open :%s----------" % i)
            dis_camera.opne_camera()#发送命令打开摄像头
            dis_camera.screen_open_ir_rgb(open_rgb_name,open_ir_name)#截图打开摄像头后的IR和RGB图
            dis_camera.close_machine()  # 关闭上位机

        except Exception as e:
            dis_camera.ScreenFile.log.logger.debug("----------test_error: %s----------" % e)
            dis_camera.close_machine()  # 关闭上位机
            time.sleep(30)

    dis_camera.ScreenFile.log.logger.debug("-----------test finish----------")
