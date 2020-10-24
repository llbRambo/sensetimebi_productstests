import hashlib
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import utils_funcs
import execjs
import jpype
from jpype import *


def md5(input):
    input = input.encode('utf-8')
    md5sign = hashlib.md5()
    md5sign.update(input)
    md5value = md5sign.hexdigest()
    return md5value


def getsign(parmas, key):
    # str1 = "languageId=0&accessToken=0E4730695CDD9B4F8D56B8107171F525-001407107122545&outTradeNo=148879135312969764307b4a86&payPlatform=dev19&packageName=com.baidu.vodx&payMode=2&price=0.01&payInfoId=15543373&version=6.2&productname=book&sourceType=dev19&thirdAppCallBack=&timeStamp=1488793412&thirdappName=com.qq.vod"
    # string 拆分为List
    strSplit = parmas.split('&')  # str.split(str="", num=string.count(str)).
    # List排序
    strSorted = sorted(strSplit)
    # List转为string，以&连接
    strConvert = '&'.join(strSorted) + '#' + key
    print(strConvert)
    sign = md5(strConvert)
    # parmasSigned=strConvert+"&sign="+sign
    return sign


def get_encodePwd(empoent, module, pwd):
    proDir = os.path.split(os.path.realpath(__file__))[0]
    file_path = os.path.join(proDir, "rsa.js")
    f = open(file_path, 'r', encoding='utf-8')  # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)  # 加载JS文件
    enPwd = (ctx.call('encodePwd', empoent, module, pwd))  # 调用js方法  第一个参数是JS的方法名，后面的是js方法的参数
    f.close()
    return enPwd


class EncryptJAVA(object):
    def __init__(self):
        if jpype.isJVMStarted():
            return
        jvmpath = getDefaultJVMPath()  # 获取默认的JVM路径
        jarPath = os.path.join(utils_funcs.encryptUtil_JarPath)
        dependency = os.path.join(utils_funcs.senselinkapi_path, "jar", 'dependency')
        jpype.startJVM(jvmpath, "-ea", "-Djava.class.path=%s" % jarPath,
                       "-Djava.ext.dirs=%s" % dependency)  # 当有依赖的JAR包存在时，一定要使用-Djava.ext.dirs参数进行引入
        # startJVM(jvmpath, "-ea", "-Djava.class.path=%s" % jarPath)
        self.encryptUtilsClass = jpype.JPackage("com.util").encryptUtils  # 实例化对象
        # print('init')

    def dec_encryptByDes(self, data, key):
        self.aes = self.encryptUtilsClass.encryptByDes(data, key)  # 调用java对象的方法
        return self.aes

    def dec_decryptByDes(self, data, key):
        self.rsa = self.encryptUtilsClass.decryptByDes(data, key)  # 调用java对象的方法
        return self.rsa

    def encryptByRSA(self, empoent, module, data):
        self.aes = self.encryptUtilsClass.encryptString(module, empoent, data)  # 调用java对象的方法
        return self.aes

    def shutdown(self):
        jpype.shutdownJVM()


encryptJAVA = EncryptJAVA()

if __name__ == "__main__":
    SECRET = "bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8"

    enString = encryptJAVA.dec_encryptByDes(data='362423194902013802', key=SECRET)
    print(enString)

    denString = encryptJAVA.dec_decryptByDes(data='TpVR4dxE63pUc8Gr1WICUYDv4tVHMTd5', key=SECRET)
    print(denString)

    denString = encryptJAVA.encryptByRSA(empoent='10001',module="d06371e3d8ae5c8eeb3de32b5045d9cc68032cf50c418be764f100518460128007e8db9ccc3a04b081e6f8755da5505dc914af49719bb55c36712af29f11a5c50a4180e0b2e6565b1b73c534ee58cbb80e31a7bd08f7558b1041c1d41b19000d50e793015379f283d96c8bbca1ad7f640c22f929d4a44a569ed701a23522245b", data="11111111")
    print(denString)
    encryptJAVA.shutdown()
