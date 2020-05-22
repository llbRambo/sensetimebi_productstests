#coding=utf-8
import time,sys,os,win32gui, win32ui, win32con,traceback
from sensetimebi_productstests.Sharedscript.SharedGetYamlConfigData import DataGetConfig
from PIL import Image
import pytesseract

class images_dispose(object):
    def __init__(self):
        '''

        '''
        getConfig = DataGetConfig()
        self.images_path = getConfig.getConfig().get("images_path")  # 获取批量添加图片地址

    def get_filenames(self,path):
        filenames = []
        for files in os.listdir(path):
            if files.endswith('jpg') or files.endswith('jpeg') or files.endswith('png') or files.endswith('JPG'):
                file = os.path.join(path, files)
                filenames.append(file)  # 获取所有图片名List
        return filenames

    def count_img(self,path):
        counts = self.get_filenames(path)
        return len(counts)

    def get_names(self,path):
        filenames = self.get_filenames(path)
        names = []
        lengs = len(path)
        for filename in filenames:
            name = filename[lengs + 1:-4]
            names.append(name)
        return names

    def imagesName(self, firstName):
        imagesName = []
        for i in range(1, 101):
            name = firstName + str(i)
            imagesName.append(name)
        return imagesName

    def rename(self, firstName):
        # 原始图片路径
        inames = self.imagesName(firstName)
        len(inames)
        # __path = 'E:\新建文件夹'
        # 获取该路径下所有图片
        fileList = os.listdir(self.images_path)
        # print(filelist)
        j = 0
        for files in fileList:
            # 原始路径
            Olddir = os.path.join(self.images_path, files)
            # print(Olddir)
            filename_img = os.path.splitext(files)[0]
            # print(filename_img)
            filetype = os.path.splitext(files)[1]
            # print(filetype)
            # 需要存储的路径 a 是需要定义修改的文件名
            Newdir = os.path.join(self.images_path, str(inames[j]) + filetype)
            os.rename(Olddir, Newdir)
            j += 1
        time.sleep(1)


    def images_str(self):
        lenghts = len(self.images_path)
        images = []
        for fileimages in os.listdir(self.images_path):
            if fileimages.endswith('jpg'):
                image = os.path.join(self.images_path, fileimages)
                name = image[lenghts + 1:]
                images.append(name)
        images = str(images)  # 字符处理
        images = images[1:-1]  # 字符处理
        images = images.replace("'", "\"")  # 字符处理
        images = images.replace(",", "")  # 字符处理
        time.sleep(1)
        return images

    def get_img_text(self,img_path):
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image,lang = "eng",
                                           config="--psm 6 --oem 3 -c tessedit-char-whitelist=0123456789").strip()
        return text

if __name__ == '__main__':
    dispose= images_dispose()
    print(dispose.count_img("D:\\test\data1"))
