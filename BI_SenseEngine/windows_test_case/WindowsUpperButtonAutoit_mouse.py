import autoit, time, random
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig

class Autoit_windows_BtnPixelCoordinate(object):
    '''
    windows上位机各个功能按钮的坐标类，以分辨率为1366X768的PC为例子
    '''

    def drag(self,x1, y1, x2, y2, button="left", speed=-1):
        '''
        :description 执行鼠标拖拽操作
        '''
        autoit.mouse_click_drag(x1, y1, x2, y2, button, speed)

    #实现鼠标点击功能
    def click(self, x, y, button="left", clicks=1, speed=-1):  # 鼠标点击
        autoit.mouse_click(button, x, y, clicks=clicks, speed=speed)
        time.sleep(0.2)

    # 点击上位机’Devices‘按钮
    def click_Device(self):
        self.click(665,333)

    # 点击上位机’Tools‘按钮
    def click_Tools(self):
        self.click(729, 333)

    # 点击上位机’Reomode‘按钮
    def click_Reomode(self):
        self.click(783, 333)

    # 点击上位机’Config‘按钮
    def click_Config(self):
        self.click(851, 333)

    # 点击上位机’Help‘按钮
    def click_help(self):
        self.click(900, 333)

    # 点击上位机二级按钮’Setting‘
    def click_Setting(self):
        self.click(683, 359)
        time.sleep(1)

    # 点击上位机’Setting‘窗口中’Select Camera‘
    def click_SelectCamera(self):
        self.click(922, 474)  # 第一次点击
        self.click(880, 487)  # 选中Uvc

    # 点击上位机’Setting‘窗口中’Select Serial Port‘
    def click_SelectSerialPort(self):
        self.click(926, 547)  # 第一次点击
        self.click(958, 598)  # 选择Uvc摄像头端口

    # 点击上位机’Setting‘窗口中’Apply‘
    def click_Apply(self):
        self.click(1029, 593)  # 点击Apply,进入上位机预览识别界面
        time.sleep(3)

    # 点击上位机二级按钮’AddBaselibraryByCamera‘，通过摄像头拍照单个添加底图
    def click_AddBaselibraryByCamera(self):
        self.click(762, 354)

    # 点击上位机二级按钮’AddBaseLibrary‘，通过导入单张图片添加底图
    def click_AddBaseLibrary(self):
        self.click(762, 381)

    # 点击上位机二级按钮’BatchAddition‘，通过批量导入图片添加底图
    def click_BatchAddition(self):
        self.click(762, 403)

    # 点击上位机二级按钮’Delete‘，单个删除底图
    def click_Delete(self):
        self.click(762, 423)

    # 点击上位机二级按钮’Delete All‘，删除整个底图库
    def click_DeleteAll(self):
        self.click(762, 447)

    # 点击上位机二级按钮’Upgrade‘，给设备升级
    def click_Upgrade(self):
        self.click(762, 470)

    # 点击上位机二级按钮’StartRecognize‘，开始识别
    def click_StartRecognize(self):
        self.click(762, 493)

    # 点击上位机二级按钮’StopRecognize‘，停止识别
    def click_StopRecognize(self):
        self.click(762, 516)

    # 点击上位机二级按钮’InputLibrary‘，导入库
    def click_InputLibrary(self):
        self.click(762, 539)

    # 点击上位机二级按钮’AddFeature‘，单个添加特征值文件
    def click_AddFeature(self):
        self.click(762, 562)

    # 点击上位机二级按钮’QueryFeature‘，单个查询特征值
    def click_QueryFeature(self):
        self.click(762, 585)

    def click_OneToNumReomode(self):
        self.click(793, 360)

    def click_OneToOneReomode(self):
        self.click(793, 383)

    def click_MultiLiving(self):
        self.click(741, 200)

    def click_MultiNoliving(self):
        self.click(741, 223)

    def click_SingleLiving(self):
        self.click(741, 250)

    def click_SingleNoliving(self):
        self.click(741, 267)

    def click_OtoMultiLiving(self):
        self.click(741, 223)

    def click_OtoMultiNoliving(self):
        self.click(741, 245)

    def click_OtosingleLiving(self):
        self.click(741, 269)

    def click_OtosingleNoLiving(self):
        self.click(741, 291)

    # 点击上位机二级按钮’SwitchCameraRGB‘，预览界面切换到RGB摄像头
    def click_SwitchCameraRGB(self):
        self.click(883, 359)

    # 点击上位机二级按钮’SwitchCameraIR‘，预览界面切换到IR摄像头
    def click_SwitchCameraIR(self):
        self.click(896, 381)

    # 点击上位机二级按钮’GetVersion‘，获取设备版本信息
    def click_GetVersion(self):
        self.click(871, 402)

    # 点击上位机二级按钮’GetLibrary‘，获取人脸库大小
    def click_GetLibrary(self):
        self.click(623, 268)

    # 点击上位机二级按钮’SetFrame‘
    def click_SetFrame(self):
        self.click(623, 290)

    def click_SetIRLight(self):
        self.click(623, 311)

    def click_GetIRlight(self):
        self.click(623, 333)

    # 点击上位机二级按钮’SetAIConfig‘，设置face ae参数
    def click_SetAIConfig(self):
        self.click(623, 358)

    # 点击上位机二级按钮’GetAIConfig‘，获取已设置的face ae参数
    def click_GetAIConfig(self):
        self.click(623, 358)

    def click_Aubot(self):
        self.click(654, 202)

    def click_ok(self):
        self.click(991, 542)

    def click_deleteErr_ok(self):
        self.click(1052, 543)

    def click_addfeature_error_ok(self):
        self.click(1100, 543)

    def click_GetImageID_OK(self):
        self.click(969, 546)

    def click_GetImageID_Cancel(self):
        self.click(1049,548)
    # 点击’Add Batch‘界面的’select Files‘按钮
    def click_SelectFilesAdd(self):
        self.click(1082, 387)

    # 点击’Add Batch‘界面的’upload‘按钮
    def click_upload(self):
        self.click(1157, 385)

    def click_add_OK(self):
        self.click(878,498)

    def click_batch_ok(self):
        self.click(1074,544)

    def click_BatchComplete_ok(self):
        self.click(1157,652)

    def click_SelectFilesUpgrade(self):
        self.click(1026,392)

    def click_UpgradeUpgrade(self):
        self.click(1111,395)

    def click_Upgrade_OK(self):
        self.click(1107,648)

    def click_BatchAdd_path(self):
        self.click(1360, 410) #批量添加点击添加路径



    def click_BatchAdd_goto(self):
        self.click(x=1426, y=411)  # 点击地址跳转

    def set_BatchAdd_images(self, images):
        autoit.control_set_text("[Title:Add Batch]", "Edit1", "%s" % images)  # 输入选中图片路径
        time.sleep(2)

    def click_BatchAdd_confirm(self):
        autoit.control_click("[Title:Add Batch]", "Button1")  # 点击确认
        time.sleep(1)

    def send(self,id):#输入ID
        autoit.send(id)
        time.sleep(0.2)

    def set_add_path(self):#单个添加图片
        autoit.control_set_text("[Title:Add Base Library]", "Edit1", self.image_path)
        time.sleep(0.2)

    def click_add_confirm(self):
        autoit.control_click("[Title:Add Base Library]", "Button1")  # 点击确认
        time.sleep(0.2)

    def set_feature_path(self):#单个特征数据
        autoit.control_set_text("[Title:Add Feature]", "Edit1", self.feature_path)
        time.sleep(0.2)

    def click_feature_confirm(self):
        autoit.control_click("[Title:Add Feature]", "Button1")  # 点击确认
        time.sleep(0.2)


    def set_Upgrade_path(self,filenames):
        autoit.control_set_text("[Title:Add Batch]", "Edit1", filenames)  # 输入升级的bin文件路径
        time.sleep(0.05)

    def click_Upgrade_confirm(self):
        autoit.control_click("[Title:Add Batch]", "Button1")  # 点击确认
        time.sleep(1)

    def click_upgrade_close(self):
        self.click(1144,355)

    def click_close(self):
        self.click(1251,305)

    def click_close_version(self):
        self.click(1093, 419)

    def wait_times(self):
        return(random.randint(10,15))

class Autoit_Upper_machine_function(Autoit_windows_BtnPixelCoordinate):
    '''
    上位机相关功能操作
    '''

    def __init__(self):
        '''
        Constructor
        '''
        getConfig = datagetConfig()
        self.pc_exe_path = getConfig.getConfig().get("pc_exe_path")  # 上位机路径
        self.images_path = getConfig.getConfig().get("images_path")  # 获取批量添加图片地址
        self.image_path = getConfig.getConfig().get("image_path")  # 获取单个添加图片地址
        self.feature_path = getConfig.getConfig().get("feature_path")  # 获取添加特征值地址

    def send_BatchAdd_path(self):
        autoit.send(self.images_path)#输入地址
        time.sleep(0.2)

    def run_active(self):
        autoit.run(self.pc_exe_path)
        autoit.win_wait_active("[CLASS:Qt5QWindowIcon]", 15)  # 等待程序打开

    def init_start(self):
        self.run_active()
        self.click_Device()  # 点击Devices
        self.click_Setting()  # 点击Setting
        self.click_SelectCamera()  # 选择Select Camera
        self.click_SelectSerialPort()  # 选择Select Serial Port
        self.click_Apply() # 点击apply
        self.click_ok()  # 异常处理点击
        time.sleep(5)

    def add_img(self,id):
        self.click_Tools() # 点击tools
        self.click_AddBaseLibrary()  # 点击add base library
        autoit.win_wait_active("[Title:Add Base Library]", 5)  # 等待页面响应
        self.set_add_path()
        self.click_add_confirm()
        self.send(id)
        self.click_GetImageID_OK()
        time.sleep(1)
        self.click_ok()

    def batchAdd_power(self,images):
        self.click_Tools()  # 点击tools
        self.click_BatchAddition()#点击Batch Addition
        autoit.win_wait_active("[CLASS:Qt5QWindowIcon]", 10)  # 等待页面响应
        self.click_SelectFilesAdd()
        autoit.win_wait_active("[CLASS:#32770]", 10)  # 等待页面响应
        self.click_BatchAdd_path()
        self.send_BatchAdd_path()
        self.click_BatchAdd_goto()
        self.set_BatchAdd_images(images)
        self.click_BatchAdd_confirm()
        self.click_upload()
        time.sleep(self.wait_times())

    def batchAdd_img(self,images):
        self.click_Tools()  # 点击tools
        self.click_BatchAddition()#点击Batch Addition
        autoit.win_wait_active("[CLASS:Qt5QWindowIcon]", 10)  # 等待页面响应
        self.click_SelectFilesAdd()
        autoit.win_wait_active("[CLASS:#32770]", 10)  # 等待页面响应
        self.click_BatchAdd_path()
        self.send_BatchAdd_path()
        self.click_BatchAdd_goto()
        self.set_BatchAdd_images(images)
        self.click_BatchAdd_confirm()
        self.click_upload()
        autoit.win_wait_active("[Title:SenseEnginie Camera]",200)  # 等待图片添加

    def click_addBatch_ok(self):
        self.click_batch_ok()
        self.click_BatchComplete_ok()

    def version_upgrade(self,upgradefile):
        self.click_Tools()
        self.click_Upgrade()
        self.click_SelectFilesUpgrade()
        autoit.win_wait_active("[Title:Add Batch]", 10)  # 等待页面响应
        self.set_Upgrade_path(upgradefile)
        self.click_Upgrade_confirm()
        self.click_UpgradeUpgrade()
        time.sleep(50)#等待文件上传

    def close_upgrade(self):
        self.click_upgrade_close()
        self.click_close()

    def delete_an(self,id):
        self.click_Tools()
        self.click_Delete()
        self.send(id)
        self.click_GetImageID_OK()
        time.sleep(0.5)
        self.click_ok()
        self.click_deleteErr_ok()

    def delete_all(self):
        self.click_Tools()
        self.click_DeleteAll()
        time.sleep(0.5)
        self.click_ok()

    def switch_rgb(self):
        self.click_Config()
        self.click_SwitchCameraRGB()

    def switch_ir(self):
        self.click_Config()
        self.click_SwitchCameraIR()

    def check_version(self):
        self.click_Config()
        self.click_GetVersion()

    def get_library(self):
        self.click_Config()
        self.click_GetLibrary()

    def Feature_init(self):
        self.delete_all()
        self.add_img("test")

    def Query_Feature(self):
        self.click_Tools()
        self.click_QueryFeature()
        self.send("test")
        self.click_GetImageID_OK()

    def Add_Feature(self,id):
        self.click_Tools()
        self.click_AddFeature()
        self.set_feature_path()
        self.click_feature_confirm()
        self.send(id)
        self.click_GetImageID_OK()
        self.click_ok()
        self.click_addfeature_error_ok()


    def check_close_port(self,):
        self.init_start()
        # 关闭并判断是否已经关闭播放器
        time.sleep(5)
        self.click_close()# 点击关闭
        time.sleep(5)

if __name__ == '__main__':
    pc_Camera_path= 'C:\\Users\senseadmin\Desktop\M20\上位机\SenseEngineCameraV3.0.1\\SenseEngineCameraV3.0.1'
    images = "D:\\test_file\\test_addAn\\test.jpg"
    # 准备数据
    getConfig = datagetConfig()
    image_path = getConfig.getConfig().get("image_path")  # 获取添加图片地址
    print(image_path)
    operation = Autoit_Upper_machine_function()
    operation.init_start()
    for i in range(1000):

        operation.add_img("test_%s"%i)
