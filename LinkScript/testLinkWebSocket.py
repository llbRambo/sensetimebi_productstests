# encoding: utf-8
import hashlib
import inspect
import json
import os
import sys
import time

import jpype
import requests
from websocket import create_connection

cur_file_path = inspect.getfile(inspect.currentframe())  # 得到定义该函数的脚本路径
path = os.path.abspath(os.path.dirname(cur_file_path))


class WebSocket():
    def __init__(self, scheme, host, account, password):
        self.scheme = scheme
        self.host = host
        self.account = account
        self.password = password
        self.timeout = 15
        self.app_key = ''
        self.app_secret = ''
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

    def login(self):
        """
        test body
        :return:
        """
        urlAppkey = self.scheme+"://"+ self.host + '/sl/v2/openapi/list'
        urlRsapub = self.scheme+"://"+ self.host + '/sl/v2/rsapub'
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
            return
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
                return
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
                        return
                    print(info)
                    if info['code'] == 200:
                        print("设备注册成功！")

                sign = self.md5("AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
                self.headers = {"LANGUAGE": LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                                "LDID": ldid, "AUTH-SIGN": sign}
                self.url = urlAppkey
                self.result = self.get()
                try:
                    info = self.result.json()
                except:
                    print(str(self.result))
                    return
                if info['code'] == 200:
                    self.app_key = info['data'][0]['app_key']
                    self.app_secret = info['data'][0]['app_secret']
                    print("获取app_key和app_secret成功！")

    def md5(self, input):
        input = input.encode('utf-8')
        md5sign = hashlib.md5()
        md5sign.update(input)
        md5value = md5sign.hexdigest()
        return md5value

    def testWebSocket(self):
        """
        test body
        :return:
        """
        self.login()
        timestamp = int(time.time() * 1000)
        sign = self.md5(str(timestamp) + "#" + self.app_secret)
        # 建立一个websocket连接
        url = "ws://" + self.host + "/websocket/record/" + self.app_key + "/" + str(timestamp) + "/" + sign
        print(url)
        ws = create_connection(url)
        data = {"app_key": self.app_key, "timestamp": timestamp, "sign": sign}
        ws.send(json.dumps(data))
        # 接返回的数据
        while (1):
            result = ws.recv()
            print(str(result))

        ws.close()


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
    obj = WebSocket(base, host, account, password)
    obj.testWebSocket()
