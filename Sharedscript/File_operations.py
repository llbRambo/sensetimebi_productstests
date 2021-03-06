import time,sys,os,win32gui, win32ui, win32con,traceback
from PIL import Image
from PIL import ImageChops
from sensetimebi_productstests.Sharedscript.Xllgoinfo import Xllgoinfo
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig
from M20.pages.Command import Command

class File_operations(object):
    # def __init__(self,__testResultFolderName):
    #     '''
    #     创建文件
    #
    #     '''
    #     self.xinfo = Xllgoinfo(__testResultFolderName)
    #     self.getConfig = DataGetConfig()

    def get_filenames(self,path):
        filenames = []
        for files in os.listdir(path):
            if files.endswith('jpg') or files.endswith('jpeg') or files.endswith('png') or files.endswith('JPG'):
                file = os.path.join(path, files)
                filenames.append(file)  # 获取所有图片名List
        return filenames

    def get_names(self,path):
        filenames = self.get_filenames(path)
        names = []
        lengs = len(path)
        for filename in filenames:
            name = filename[lengs + 1:-4]
            names.append(name)
        return names

    #创建文件夹
    def create_floder(self, flodername, SpecifyPath=sys.path[0]):   #默认在脚本当前目录下创建文件夹
        filepath = str(SpecifyPath) + '\\' + str(flodername) + '\\'
        folder = os.path.exists(filepath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            print("---  创建新的文件夹...  ---")
            os.makedirs(filepath)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  OK  ---")
        else:
            print("---  文件夹已存在!  ---")
        return filepath

    # 创建文件
    def create_file(self, flodername, filename):
        # gettime = time.strftime('%Y-%m-%d', time.gmtime())  # 获得当前时间的列表
        gettime = time.strftime('%Y-%m-%d', time.gmtime())  # 获得当前时间的列表
        filepath = str(sys.path[0]) + '\\' + str(flodername) + '\\' + str(gettime) + str(filename)
        folder = os.path.exists(filepath)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            print("---  创建新的文件...  ---")
            os.makedirs(filepath)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---  OK  ---")
        else:
            print("---  文件已存在!  ---")
        return filepath


    def window_capture(self,filename):
        """
                截取windows系统活动窗口
        """
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

    def compare_images(self, path_one, path_two, box=None):
        """
                比较图片是否一样
        @path_one: 第一张图片的路径
        @path_two: 第二张图片的路径

        """
        #box = self.getConfig.getConfig().get("pic_comared_coordinate")
        box = (12, 8, 360, 400)
        times = time.ctime()
        image_one = Image.open(path_one).crop(box)
        image_two = Image.open(path_two).crop(box)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                result = [times, "Two pictures are the same."]
                self.xinfo.log_info(result)
                return True
            else:
                result = [times, "Two pictures are the different."]
                self.xinfo.log_info(result)
                return False
        except:
            traceback.print_exc()
            result = [times, "-----compare_images Error-----"]
            self.xinfo.log_info(result)
            return False

    def imagesName(self,firstName):
        imagesName = []
        for i in range(1, 101):
            name = firstName + str(i)
            imagesName.append(name)
        return imagesName

    def rename(self,firstName, img_path):
        # 原始图片路径
        inames = self.imagesName(firstName)
        len(inames)
        # __path = 'E:\新建文件夹'
        # 获取该路径下所有图片
        fileList = os.listdir(img_path)
        #print(filelist)
        j = 0
        for files in fileList:
            # 原始路径
            Olddir = os.path.join(img_path, files)
            # print(Olddir)
            filename_img = os.path.splitext(files)[0]
            # print(filename_img)
            filetype = os.path.splitext(files)[1]
            # print(filetype)
            # 需要存储的路径 a 是需要定义修改的文件名
            Newdir = os.path.join(img_path, str(inames[j]) + filetype)
            os.rename(Olddir, Newdir)
            j += 1

    def images_str(self,img_path):
        lenghts = len(img_path)
        images = []
        for fileimages in os.listdir(img_path):
            if fileimages.endswith('jpg'):
                image = os.path.join(img_path,fileimages)
                name = image[lenghts+1:]
                images.append(name)
        images = str(images)#字符处理
        images = images[1:-1]#字符处理
        images = images.replace("'","\"")#字符处理
        images = images.replace(",","")#字符处理
        return images

if __name__ == '__main__':
    getConfig = DataGetConfig()
    box = getConfig.getConfig().get("pic_comared_coordinate")
    print(box)