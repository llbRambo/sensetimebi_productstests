#-- coding: utf-8 --
import uiautomator2 as u2
import os
import re
import time
import sys
from sensetimebi_productstests.Sharedscript.logger import Logger

class SenseEngineCameraDemoDebugApk(object):

    def __init__(self, ipport, LogStorageAddress):
        #类内参数赋值
        self.__success_count = 0
        self.__fail_count = 0
        self.__ipport = ipport
        self.__LogStorageAddress = LogStorageAddress

        #创建log文件，并且将log写入文件
        self.filepath = self.__LogStorageAddress + time.strftime('%y%m%d_%H%M%S') + '.txt' #创建测试结果日志文件名字
        self.log = Logger(self.filepath, level='debug') #将测试日志写入日志文件

        #对安卓设备进行连接
        self.d = u2.connect_adb_wifi(self.__ipport)  # 连接安卓设备



    def init_devices(self):
        return u2.connect_adb_wifi(self.__ipport)

    def screen_img(self, img_path, img_name):
        self.d.screenshot(img_path + img_name) #截取设备所在界面的图片
        time.sleep(1)


    '''
    关于安卓上位机apk的功能实现函数
    '''
    def start_app(self):
        self.d.app_start("com.sensetime.demo", "com.sensetime.demo.ui.SplashActivity")
        time.sleep(2)

    #根据apk名来停止apk
    def stop_app(self, appName):
        # 检查上位机是否存在，如果存在，则杀掉
        info = os.popen('adb -s %s shell ps ' % self.__ipport).read()
        # print('info')
        # print(info)
        flag = info.find(appName)
        # print('flag: ', flag)
        if flag != -1:
            self.log.logger.debug('进程存在，杀掉进程！！！')
            self.d.app_clear(appName)
            self.log.logger.debug('杀进程成功！！！')
        else:
            self.log.logger.debug('进程不存在！！！')



    #点击系统返回键
    def back_button(self):
        '''
        点击返回
        :return:
        '''
        self.d(resourceId="com.android.systemui:id/back").click()
        time.sleep(1)

    def close_initiative_upload(self):
        '''
        检查识别数据上报模式，关闭主动上报
        :return:
        '''
        self.d(resourceId="com.sensetime.demo:id/choose_upload_mode").click()
        time.sleep(2)
        if self.d(text="主动上报 开启").exists():
            self.d(resourceId="com.sensetime.demo:id/switch_initiative_upload").click()
            time.sleep(0.5)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        # elif self.d(text="帧数据携带人脸识别数据 开启").exists():
        #     time.sleep(0.5)
        #     self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()


    def check_Report_switch(self):
        '''
        检查识别数据上报模式，确认帧数开关打开
        :return:
        '''
        self.d(resourceId="com.sensetime.demo:id/choose_upload_mode").click()
        time.sleep(2)
        if self.d(text="帧数据携带人脸识别数据 关闭").exists():
            self.d(resourceId="com.sensetime.demo:id/switch_frame_upload").click()
            time.sleep(0.5)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        elif self.d(text="帧数据携带人脸识别数据 开启").exists():
            time.sleep(0.5)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()

    #进入预览界面
    def into_preview(self):
        self.d(resourceId="com.sensetime.demo:id/entry_cam_btn").click()
        time.sleep(0.5)
        try:
            self.d(resourceId="android:id/button1").click()
            time.sleep(1)
        except:
            time.sleep(1)
        else:
            try:
                self.d(resourceId="com.android.packageinstaller:id/permission_allow_button").click()
                time.sleep(5)
            except:
                time.sleep(5)

    #点击预览界面“设置”按钮
    def setting(self):
        '''
        设置
        :return:
        '''
        self.d(resourceId="com.sensetime.demo:id/btn_setting").click()
        time.sleep(2)

    def Photo_add(self,id):
        '''
        拍照添加
        :param id:
        :return:
        '''
        self.d(resourceId="com.sensetime.demo:id/main_add_image_by_camera_btn").click()
        time.sleep(0.5)
        self.d(resourceId="android:id/input").set_text(id)  # 输入ID
        time.sleep(0.5)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()

    def delete_user(self,id):
        '''
        删除指定用户
        :param id:
        :return:
        '''
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/setting_del_user_btn").click()
        time.sleep(0.5)
        self.d(resourceId="android:id/input").set_text(id)  # 输入ID
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        time.sleep(0.5)
        self.back_button()

    def delete_all(self):
        '''
        删除所有用户
        :return:
        '''
        self.log.logger.debug("----------删除所有---------")
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/setting_del_all_user_btn").click()
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        time.sleep(1)
        self.back_button()
        time.sleep(2)

    def add_an_user(self,id):
        '''
        添加单个用户
        :return:
        '''
        self.setting() #点击预览界面的“设置”按钮
        time.sleep(3)
        self.d(resourceId="com.sensetime.demo:id/setting_batch_add_user_btn").click() #点击添加用户
        self.d.xpath('//*[@resource-id="com.sensetime.demo:id/list"]/android.widget.FrameLayout[1]/android.widget.ImageView[1]'
                     ).click()#选择图片
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/tv_finish").click()#点击完成
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/user_id_et").set_text(id)  # 输入ID
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click() #输入ID之后点击确定
        time.sleep(2)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click() #添加用户执行成功之后点击确定

        time.sleep(10)
        self.back_button() #点击系统返回键，回到预览界面
        time.sleep(10)

    def add_batch_user(self,img_path, img_name):
        '''
        添加单个用户
        :return:
        '''
        self.log.logger.debug("----------批量添加----------")
        self.setting()#点击设置
        self.d(resourceId="com.sensetime.demo:id/setting_batch_add_user_btn").click()#点击添加用户
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/tv_full_select").click()#点击全选
        time.sleep(0.5)
        self.d(resourceId="com.sensetime.demo:id/tv_finish").click()#点击完成
        time.sleep(0.5)
        if self.d(text="选了：1000").exists(timeout = 5):
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
            self.log.logger.debug("----------选中1000张----------")
        else:
            self.log.logger.debug("----------没有选中所有--------")
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
        time.sleep(1)
        try:
            self.d(text="执行成功: 1000 执行失败: 0").exists(6*60)  # 等待文件上传成功
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
            self.__success_count += 1
            self.log.logger.debug("----------添加成功----------%s" % self.__success_count)
        except:
            self.__fail_count+=1
            self.log.logger.debug("----------添加失败----------%s" % self.__fail_count)
            self.screen_img(img_path, img_name)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
        time.sleep(1)
        self.back_button()
        time.sleep(2)


    #统计bin文件传输时间
    def upgradetime(self, i, img_path, img_name, bin_name):
        upgrade_flag = False
        '''固件升级'''
        self.log.logger.debug("---------固件升级----------test %s" % i)
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/setting_upgrade_firmware_btn").click()  # 升级固件
        time.sleep(0.5)
        if self.d(text=bin_name).exists():    #检测所选软件版本是否为目标版本
            self.d.xpath('//*[@text="' + bin_name + '"]').click()  # 升级固件
            self.log.logger.debug("当前选择固件为：%s" % bin_name)
        else:
            self.log.logger.debug("---------找不到目标升级文件----------")
            exit(1)
        time.sleep(0.5)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
        start_time = time.time()  #bin文件传输开始时间
        try:
            while upgrade_flag == False:
                upgrade_flag = self.d(text="执行成功,设备将重启,稍等1分钟,杀掉整个应用进程，然后请重新去启动应用").exists(150)  # 150秒内查询文件是否上传成功，150秒内没有成功则报错
                # print('upgrade_flag: ', upgrade_flag)
                if upgrade_flag:
                    end_time = time.time() #bin文件传输结束时间
                    upload_bin_time = end_time - start_time  #bin文件传输总共花费时间
                    time.sleep(0.5)
                    self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
                    self.log.logger.debug("文件上传时间为：%s" % upload_bin_time)
                    self.log.logger.debug("---------升级成功----------")
        except:
            self.log.logger.debug("---------升级失败----------")
            self.screen_img(img_path, img_name)
            time.sleep(0.5)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()  # 点击确认
        time.sleep(100) #等待设备启动
        #如果上位机仍然存在，在下次测试之前需要杀掉上位机
        appName = 'com.sensetime.demo'
        self.stop_app(appName)  # 杀掉上位机


    def get_feature(self,id):
        self.log.logger.debug("---------获取特征值----------")
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/get_features_btn").click()
        time.sleep(0.5)
        self.d(resourceId="android:id/input").set_text(id)  # 输入ID
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        time.sleep(0.5)
        self.back_button()
        time.sleep(2)

    def add_feature(self, id):
        self.log.logger.debug("---------添加特征值----------")
        time.sleep(1)
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/add_features_btn").click()
        time.sleep(0.5)
        self.d(resourceId="android:id/input").set_text(id)  # 输入ID
        time.sleep(1)
        add_feature_flag = False
        while add_feature_flag != True:
            add_feature_flag = self.d(text="请确保你已经获取到了特征值").exists(10)
            if add_feature_flag:
                self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        time.sleep(1)
        self.back_button() #点击
        time.sleep(2)

    def reboot_system(self,i,img_path, img_name):
        self.log.logger.debug("---------重启系统----------test %s"%i)
        self.setting()
        self.d(resourceId="com.sensetime.demo:id/reboot_system_btn").click()
        time.sleep(1)
        self.d(resourceId="com.sensetime.demo:id/md_title", text="直接重启").click()
        time.sleep(0.5)
        self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
        time.sleep(60)
        self.stop_app()
        self.start_app()
        self.check_Report_switch()
        self.into_preview()
        time.sleep(1)
        self.screen_img(img_path, img_name)
        time.sleep(1)

    def recognition(self,pause_img_path, pause_img_name,resetore_img_path, resetore_img_name,i):
        if self.d(text="暂停识别").exists():
            self.log.logger.debug("---------暂停识别----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/btn_disregard", text="暂停识别").click()
            time.sleep(3)
            self.screen_img(pause_img_path, pause_img_name)
            time.sleep(1)
        elif self.d(text="恢复识别").exists():
            self.log.logger.debug("---------恢复识别----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/btn_disregard", text="恢复识别").click()
            time.sleep(3)
            self.screen_img(resetore_img_path, resetore_img_name)
            time.sleep(1)

    def swtich_IR(self,ir_camera_path, ir_camera_name):
            self.d(text="RGB摄像头").exists()
            self.log.logger.debug("---------切换IR摄像头----------")
            self.d(resourceId="com.sensetime.demo:id/btn_ir_rgb_mode").click()
            time.sleep(2)
            self.screen_img(ir_camera_path,ir_camera_name)
            time.sleep(1)

    def swtich_RGB(self,rgb_camera_path, rgb_camera_name):
            self.d(text="IR摄像头(M20)").exists()
            self.log.logger.debug("---------切换RGB摄像头----------")
            self.d(resourceId="com.sensetime.demo:id/btn_ir_rgb_mode").click()
            time.sleep(2)
            self.screen_img(rgb_camera_path,rgb_camera_name)
            time.sleep(1)

    def onoff_camera(self,i,close_ir_camera_path, close_ir_camera_name,close_rgb_camera_path, close_rgb_camera_name,open_ir_camera_path, open_ir_camera_name,open_rgb_camera_path, open_rgb_camera_name):
        time.sleep(2)
        self.d(resourceId="com.sensetime.demo:id/camera_statues_btn").click()
        time.sleep(1)
        if self.d(text="RGB摄像头 开启").exists() and self.d(text="IR摄像头(M20) 开启").exists():
            self.log.logger.debug("---------关闭RGB摄像头----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/rgb_camera_statues_switch").click()
            time.sleep(3)
            self.log.logger.debug("---------关闭IR摄像头----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/ir_camera_statues_switch").click()
            time.sleep(3)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
            time.sleep(1)
            self.swtich_IR(close_ir_camera_path,close_ir_camera_name)
            self.swtich_RGB(close_rgb_camera_path,close_rgb_camera_name)

        elif self.d(text="RGB摄像头 关闭").exists() and self.d(text="IR摄像头(M20) 关闭").exists():
            self.log.logger.debug("---------打开RGB摄像头----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/rgb_camera_statues_switch").click()
            time.sleep(10)
            self.log.logger.debug("---------打开IR摄像头----------test %s"%i)
            self.d(resourceId="com.sensetime.demo:id/ir_camera_statues_switch").click()
            time.sleep(1.5)
            self.d(resourceId="com.sensetime.demo:id/md_buttonDefaultPositive").click()
            time.sleep(1)
            self.swtich_IR(open_ir_camera_path, open_ir_camera_name)
            self.swtich_RGB(open_rgb_camera_path, open_rgb_camera_name)

if __name__ == '__main__':
    ip = "10.9.40.82:8888"
    D = SenseEngineCameraDemoDebugApk(ip, "拍照添加")
    close_ir_camera_path = D.create_file("关闭IR预览界面截图") + "\\"
    close_rgb_camera_path = D.create_file("关闭RGB预览界面截图") + "\\"
    open_ir_camera_path = D.create_file("打开IR预览界面截图") + "\\"
    open_rgb_camera_path = D.create_file("打开rgb预览界面截图") + "\\"
    for i in range(1,10000):
        close_ir_camera_name = "close_ir_%s.jpg"%i
        close_rgb_camera_name = "close_rgb_%s.jpg"%i
        open_ir_camera_name = "open_ir_%s.jpg"%i
        open_rgb_camera_name = "open_rgb_%s.jpg"%i
        D.onoff_camera(i,close_ir_camera_path,close_ir_camera_name,close_rgb_camera_path,close_rgb_camera_name
                       ,open_ir_camera_path,open_ir_camera_name,open_rgb_camera_path,open_rgb_camera_name)
        D.onoff_camera(i, close_ir_camera_path, close_ir_camera_name, close_rgb_camera_path, close_rgb_camera_name
                       , open_ir_camera_path, open_ir_camera_name, open_rgb_camera_path, open_rgb_camera_name)




