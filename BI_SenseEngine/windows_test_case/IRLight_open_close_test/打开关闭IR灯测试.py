from BI_SenseEngine.ShareScripts.Screenshots_operation import Screenshots_operation
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose
from BI_SenseEngine.ShareScripts.service_serial import M20_serial
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
import time

class operation_IR(object):
    def __init__(self):
        # 准备数据
        getConfig = datagetConfig()
        close_ir_led = getConfig.getConfig().get("close_ir_led")#关闭IR灯
        open_ir_led = getConfig.getConfig().get("open_ir_led")#打开IR灯
        equipment_port = getConfig.getConfig().get("equipment_port")  # 获取设备串口号
        # 引用公共类
        self.imgdis = images_dispose()
        self.ScreenFile = Screenshots_operation("打开关闭IR灯测试结果")
        self.equipment_ser = M20_serial(port=equipment_port, baudrate=115200)
        self.operation = Autoit_Upper_machine_function()
        # 准备命令
        self.close_IrLed = self.equipment_ser.asc_str(close_ir_led)#关闭IR灯
        self.open_IrLed = self.equipment_ser.asc_str(open_ir_led)#打开IR灯
        stop_ai = '''ubus call ai ai_stop '{"prod_type":1}' '''
        self.ai_stop = self.equipment_ser.asc_str(stop_ai)
        # 创建图片存放地址
        self.open_ir_img = self.ScreenFile.create_file('打开RGB图片') + "\\"
        self.close_ir_img = self.ScreenFile.create_file('关闭RGB图片') + "\\"


    def ir_init(self):
        '''
        打开上位机切换IR摄像头关闭算法
        :return:
        '''
        self.operation.init_start()  # 打开上位机
        self.operation.switch_ir()#切换成ir识别
        time.sleep(1)
        #self.equipment_ser.send_cmd(self.ai_stop)#关闭FACE
        #time.sleep(1)

    def close_screen_ir(self,close_name):
        '''
        关闭IR并截图
        '''
        self.equipment_ser.send_cmd(self.close_IrLed)
        time.sleep(0.5)
        self.ScreenFile.window_capture(ir_dis.close_ir_img + close_name)

    def open_screen_ir(self,open_name):
        '''
        打开IR并截图
        :return:
        '''
        self.equipment_ser.send_cmd(self.open_IrLed)
        time.sleep(0.5)
        self.ScreenFile.window_capture(ir_dis.open_ir_img + open_name)


if __name__ == '__main__':
    test_max = 10000

    ir_dis = operation_IR()
    ir_dis.ScreenFile.log.logger.debug("----------test start----------")
    ir_dis.ir_init()#打开上位机切换IR摄像头关闭FACE

    for i in range(1,test_max):
        ir_dis.ScreenFile.log.logger.debug("----------test: %s----------"%i)
        try:
            #关闭IR灯
            ir_dis.ScreenFile.log.logger.debug("----------test_close: %s----------" % i)
            close_name = 'close_ir_%s.jpg'%i
            ir_dis.close_screen_ir(close_name)#关闭IR并截图

            time.sleep(5)

            #打开IR灯
            ir_dis.ScreenFile.log.logger.debug("----------test_opne: %s----------" % i)
            open_name = 'open_ir_%s.jpg' % i
            ir_dis.open_screen_ir(open_name)  # 关闭IR并截图

            time.sleep(5)
            ir_dis.operation.click_ok()
        except Exception as e:
            ir_dis.ScreenFile.log.logger.debug("----------test_error: %s----------" % e)
            time.sleep(30)

    ir_dis.ScreenFile.log.logger.debug("-----------test finish----------")


