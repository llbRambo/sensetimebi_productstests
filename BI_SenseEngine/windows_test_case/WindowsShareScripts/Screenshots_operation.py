#coding=utf-8

import time,sys,os,win32gui, win32ui, win32con,traceback,io,re
from PIL import Image
from PIL import ImageChops
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
from BI_SenseEngine.ShareScripts.logger import Logger
from BI_SenseEngine.windows_test_case.WindowsUpperButtonAutoit_mouse import Autoit_Upper_machine_function
from BI_SenseEngine.ShareScripts.images_dispose import images_dispose


class Screenshots_operation(object):

    def __init__(self,resultname):
        '''
        创建文件并且截图
        '''
        self.getConfig = datagetConfig()
        path = "D:\\test\\test_result\\log_%s"%resultname + time.strftime('%m%d_%H%M%S') + '.txt'
        self.log = Logger(path, level='debug')
        self.upper_dis = Autoit_Upper_machine_function()
        self.img_dis = images_dispose()

    def create_file(self, fendsWith):
        gettime = time.strftime('%Y-%m-%d', time.gmtime())  # 获得当前时间的列表
        gettime = str(gettime + fendsWith)
        getpath = str(sys.path[0]) + self.getConfig.getConfig().get("screen_path") + gettime
        try:
            if (os.path.exists(gettime)):
                pass
                # print("文件已存在")
                # os.removedirs(getpath)#空目录删除成功
            else:
                os.mkdir(str(sys.path[0]) + self.getConfig.getConfig().get("screen_path") + gettime)
        except:
            print('文件创建失败,文件已经存在')
        # print(getpath)
        return getpath

    def window_capture(self,filename):
        """
                截取windows系统活动窗口
        """
        time.sleep(2)
        hwnd = win32gui.GetForegroundWindow()
        #         hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        l, t, r, b = win32gui.GetWindowRect(hwnd)
        w = r - l
        h = b - t
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)
        time.sleep(1)

    def compare_images(self, path_one, path_two, box=None):
        """
                比较图片是否一样
        @path_one: 第一张图片的路径
        @path_two: 第二张图片的路径

        """
        #box = self.getConfig.getConfig().get("pic_comared_coordinate")
        box = (12, 8, 360, 400)
        image_one = Image.open(path_one).crop(box)
        image_two = Image.open(path_two).crop(box)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                self.log.logger.debug("Two pictures are the same.")
                return True
            else:
                self.log.logger.debug("Two pictures are the different.")
                return False
        except:
            traceback.print_exc()
            Logger('error.log', level='error').logger.error("-----compare_images Error-----")
            return False

    def screnn_vension(self,filename):#获取当前版本并判断输出版本号
        self.upper_dis.click_Config()
        self.upper_dis.click_GetVersion()
        self.window_capture(filename)
        #sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
        vension_string = self.img_dis.get_img_text(str(filename))
        strings = "software version"
        flag = True
        try:
            vensions = re.findall(r"software version=(.+?)\n",vension_string)
            vension = vensions[0]
            if strings in vension_string:
                self.upper_dis.click_close_version()
                self.log.logger.debug("----------当前版本：%s--------"%vension)
                flag = True
        except:
            self.upper_dis.click_ok()
            self.log.logger.debug("----------当前没有获取到版本--fail-%s----------"%vension_string)
            flag = False
        return flag

    def screen_upload(self,upgradefile,filename):
        self.upper_dis.version_upgrade(upgradefile)
        self.window_capture(filename)
        self.upper_dis.close_upgrade()

if __name__ == '__main__':
    time.sleep(3)
    version_number = '2.10'

    ScreenFile = Screenshots_operation("log_BattchAddition测试结果.txt")
    # version_img = ScreenFile.create_file("版本查询截图文件") + "\\"  # 创建图片存在的文件夹
    # ScreenFile.window_capture(version_img + 'version.jpg')
    # version_img_path = str(version_img+ 'version.jpg')
    ScreenFile.screnn_vension("1.png")