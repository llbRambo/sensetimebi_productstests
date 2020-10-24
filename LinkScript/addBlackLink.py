# encoding: utf-8
import hashlib
import inspect
import os
import random
import string
import sys
import time

import jpype
import requests

cur_file_path = inspect.getfile(inspect.currentframe())  # 得到定义该函数的脚本路径
path = os.path.abspath(os.path.dirname(cur_file_path))


class addBlackLink():
    def __init__(self, scheme, host, account, password, groupid, path):
        self.scheme = scheme
        self.host = host
        self.account = account
        self.password = password
        self.timeout = 15
        self.path = path
        self.groupid = groupid
        self.url = ''
        self.headers = {}
        self.params = {}
        self.data = {}
        self.array = None
        self.url = None
        self.files = {}
        self.state = 0
        self.result = None
        self.timestamp = int(time.time() * 1000)
        self.SECRET = "bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8"

    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(self.timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            print("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file
    def post(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=self.data,
                                     timeout=float(self.timeout), verify=False)
            # response.raise_for_status()
            return response
        except TimeoutError:
            print("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(self.timeout), verify=False)
            return response
        except TimeoutError:
            print("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(self.timeout),
                                     verify=False)
            # print(self.data)
            return response
        except TimeoutError:
            print("Time out!")
            return None

    def addUser(self):
        """
        test body
        :return:
        """
        # set url
        urlAddBlack = self.scheme+"://" + self.host + '/api/v2/black'
        urlAppkey = self.scheme+"://" + self.host + '/sl/v2/openapi/list'
        urlRsapub = self.scheme+"://" + self.host + '/sl/v2/rsapub'
        urlLogin = self.scheme+"://" + self.host + '/sl/v2/device/login'
        urlRegister = self.scheme+"://" + self.host + '/sl/v2/device/register'

        LANGUAGE = 'zh'
        self.headers = {"LANGUAGE": LANGUAGE}
        self.url = urlRsapub
        self.result = self.get()
        try:
            info = self.result.json()
        except:
            print(str(self.result))
        print(info)

        if info['code'] == 200:
            print("获取Rsapub成功！")
            empoent = info['data']['empoent']
            module = info['data']['module']
            rsaId = info['data']['rsa_id']
            pw = encryptJAVA.encryptByRSA(empoent, module, self.password)

            self.data = {"account": self.account, "password": pw, "rsa_id": rsaId, "identifier": 'SPS', "duid": "1"}
            self.url = urlLogin
            #           print(self.data)
            self.result = self.postWithJson()
            try:
                info = self.result.json()
            except:
                print(str(self.result))
            if info['code'] == 200:
                token = info['data']['token']
                ldid = info['data']['device']['ldid']
                print("设备登录成功！")
                if info['data']['newDeviceKey']:
                    sign = self.md5(
                        "AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
                    self.headers = {"LANGUAGE": LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                                    "LDID": ldid,
                                    "AUTH-SIGN": sign}
                    self.data = {"name": "1", "direction": 2, "location": "xlplocation_",
                                 "description": "description", "software_version": "v2.2.2", "info": "info"}
                    self.url = urlRegister
                    #                    print(self.data)
                    self.result = self.postWithJson()
                    try:
                        info = self.result.json()
                    except:
                        print(str(self.result))
                    print(info)
                    if info['code'] == 200:
                        print("设备注册成功！")

                sign = self.md5("AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
                self.headers = {"LANGUAGE": LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                                "LDID": ldid, "AUTH-SIGN": sign, "Referer": "http://www.sensetime.com"}
                self.url = urlAppkey
                self.result = self.get()
                info = self.result.json()
                if info['code'] == 200:
                    app_key = info['data'][0]['app_key']
                    app_secret = info['data'][0]['app_secret']
                    print("获取app_key和app_secret成功！")
                    print("开始添加黑名单")
                    i = 0

                    for root, dirs, files in os.walk(self.path):
                        dirs.sort()
                        for file in files:
                            # 添加黑名单
                            self.timestamp = int(time.time() * 1000)
                            name = file.split('.')[0]
                            print('文件--' + file)
                            idNumber = self.idcard_generator()
                            mobile = self.phone_generator()
                            number = self.Number(10)
                            sign = self.md5(str(self.timestamp) + '#' + app_secret)
                            self.data = {'name': 'blackAPI_' + str(self.timestamp), 'mobile': mobile,
                                         'groups': [self.groupid], 'areaCode': '86', 'gender': 1, 'icNumber': number,
                                         'birthday': idNumber[1], 'idNumber': idNumber[0], 'prompt': 'welcome_black',
                                         'remark': 'black_OpenAPI',
                                         "app_key": app_key, "timestamp": self.timestamp, "sign": sign}
                            self.url = urlAddBlack
                            # print(self.data)
                            if file != '':
                                start = int(time.time() * 1000)
                                f = open(self.path + '/' + file, "rb")
                                self.files = {'avatarFile': (file, f, "image/jpeg")}
                                self.result = self.postWithFile()
                                try:
                                    info = self.result.json()
                                except:
                                    print(str(self.result))
                                    continue
                                end = int(time.time() * 1000)
                                print(info)
                                print('耗时：' + str(end - start) + 'ms')
                                if info['code'] == 200:
                                    i += 1
                                    print("添加黑名单(" + name + ")成功——total：" + str(i))
                                time.sleep(0.1)
                                f.close()
                    print("总添加黑名单：" + str(i) + '个')

    def md5(self, input):
        input = input.encode('utf-8');
        md5sign = hashlib.md5()
        md5sign.update(input)
        md5value = md5sign.hexdigest()
        return md5value

    def birthdayGenerator(self):
        '''生成年份'''
        now = time.strftime('%Y')
        # 1948为第一代身份证执行年份,now-18直接过滤掉小于18岁出生的年份
        year = random.randint(1948, int(now) - 18)

        '''生成月份'''
        month = random.randint(1, 12)
        # 月份小于10以下，前面加上0填充
        if month < 10:
            month = '0' + str(month)
        '''生成日期'''
        day = random.randint(1, 28)
        # 日期小于10以下，前面加上0填充
        if day < 10:
            day = '0' + str(day)
        birthday = str(year) + '-' + str(month) + '-' + str(day)
        # print('随机生成的日期为：'+birthday)
        return birthday

    def idcard_generator(self):
        first_list = ['362402', '362421', '362422', '362423', '362424', '362425', '362426', '362427', '362428',
                      '362429', '362430', '362432', '110100', '110101', '110102', '110103', '110104', '110105',
                      '110106', '110107', '110108', '110109', '110111']
        first = random.choice(first_list)

        birthday = self.birthdayGenerator()

        '''生成身份证后四位'''
        # 后面序号低于相应位数，前面加上0填充
        last = random.randint(1, 9999)
        if last < 10:
            last = '000' + str(last)
        elif 10 < last < 100:
            last = '00' + str(last)
        elif 100 < last < 1000:
            last = '0' + str(last)

        IDcard = str(first) + birthday + str(last)
        # print('随机生成的身份证号码为：'+IDcard)
        return [IDcard.replace('-', ''), birthday]

    def phone_generator(self):

        num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187',
                     '188',
                     '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits, 8))
        phone = start + end
        # print('随机生成的手机号为：' + phone)
        return phone

    def Number(self,len):
        Number = ''.join(random.sample(string.digits, len))
        return Number


class EncryptJAVA(object):
    def __init__(self):
        if jpype.isJVMStarted():
            return
        jvmpath = jpype.getDefaultJVMPath()  # 获取默认的JVM路径
        jarPath = os.path.join(path, "jar", "encryptUtils.jar")
        dependency = os.path.join(path, "jar", 'dependency')
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
    base=sys.argv[1]
    host = sys.argv[2]
    account = sys.argv[3]
    password = sys.argv[4]
    groupid = sys.argv[5]
    path = sys.argv[6]
    obj = addBlackLink(base, host, account, password, int(groupid), path)
    obj.addUser()
