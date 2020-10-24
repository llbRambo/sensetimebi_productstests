# encoding: utf-8
import hashlib
import inspect
import os
import sys
import time

import jpype
import requests

cur_file_path = inspect.getfile(inspect.currentframe())  # 得到定义该函数的脚本路径
path = os.path.abspath(os.path.dirname(cur_file_path))


class moveGroupUser():
    def __init__(self, scheme, host, account, password, groupFrom, groupTo, n):
        self.scheme = scheme
        self.host = host
        self.account = account
        self.password = password
        self.timeout = 15
        self.groupFrom = groupFrom
        self.groupTo = groupTo
        self.n = n
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

    def moveGroupUser(self):
        """
        test body
        :return:
        """
        # set url
        urlGroupUser = self.scheme+"://" + self.host + '/sl/v2/group/sync'  #获取组内所有用户ID
        urlAddGroupUser = self.scheme+"://" + self.host + '/api/v1/user/add/group'  #批量添加人员到组
        urlRemoveGroupUser = self.scheme+"://"+ self.host + '/api/v1/user/remove/group'  #从组中批量移出人员

        urlAppkey = self.scheme+"://"+ self.host + '/sl/v2/openapi/list'  #获取openapi列表
        urlRsapub = self.scheme+"://"+ self.host + '/sl/v2/rsapub'  #RSA密钥获取
        urlLogin = self.scheme+"://" + self.host + '/sl/v2/device/login'  #设备登录
        urlRegister = self.scheme+"://" + self.host + '/sl/v2/device/register'  #设备注册

        LANGUAGE = 'zh'
        self.headers = {"LANGUAGE": LANGUAGE}
        self.url = urlRsapub
        self.result = self.get()
        try:
            info = self.result.json()
            print('获取密钥的反馈： ', info)
        except:
            print(str(self.result))
            return


        if info['code'] == 200:
            print("获取Rsapub成功！")
            empoent = info['data']['empoent']
            module = info['data']['module']
            rsaId = info['data']['rsa_id']
            pw = encryptJAVA.encryptByRSA(empoent, module, self.password)

            self.data = {"account": self.account, "password": pw, "rsa_id": rsaId, "identifier": 'SPS', "duid": "1"}
            self.url = urlLogin
            # print(self.data)
            self.result = self.postWithJson()
            try:
                info = self.result.json()
                print('登陆的反馈： ', info)
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
                    #  print(self.data)
                    self.result = self.postWithJson()
                    try:
                        info = self.result.json()
                        print('注册的反馈： ', info)
                    except:
                        print(str(self.result))
                        return
                    # print(info)
                    if info['code'] == 200:
                        print("设备注册成功！")

                sign = self.md5("AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
                self.headers = {"LANGUAGE": LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                                "LDID": ldid, "AUTH-SIGN": sign}
                self.url = urlAppkey
                self.result = self.get()
                try:
                    info = self.result.json()
                    print('获取openapi反馈： ', info)
                except:
                    print(str(self.result))
                    return
                if info['code'] == 200:
                    app_key = info['data'][0]['app_key']
                    app_secret = info['data'][0]['app_secret']
                    print("获取app_key和app_secret成功！")

                    # 获取组内userID
                    self.params = {"group_id": self.groupFrom}  # self.groupFrom
                    self.url = urlGroupUser
                    self.result = self.get()
                    try:
                        info = self.result.json()
                        print('获取组内员工id反馈： ', info)
                    except:
                        print(str(self.result))
                        return
                    # print(info)
                    i = 0
                    userids = []
                    userList = info['data']
                    print('获取组内ID共' + str(len(userList)) + '个')
                    if self.n > len(userList):
                        self.n = len(userList)
                    for userid in userList:
                        userids.append(str(userid['user_id']))  #
                        i += 1
                        if i == self.n:
                            break
                    userList = self.trans_data_to_pair(userids, 50)

                    for i in range(len(userList)):
                        # 往组里添加人员
                        self.timestamp = int(time.time() * 1000)  #时间戳处理
                        self.headers = {"Referer": "http://www.sensetime.com"}
                        sign = self.md5(str(self.timestamp) + '#' + app_secret)  #签名
                        self.data = {"groupId": self.groupTo, "userIds": userList[i], "app_key": app_key,
                                     "timestamp": self.timestamp, "sign": sign}
                        # print('发送请求：'+str(self.data))
                        self.url = urlAddGroupUser
                        self.result = self.post()
                        try:
                            info = self.result.json()
                            print('更新组人员反馈： ', info)
                        except:
                            print(str(self.result))
                        # print(info)
                        if info['code'] == 200:
                            print("批量添加人员到组成功:" + str(len(userList[i])))

                        # 从组里移除人员
                        self.data = {"groupId": self.groupFrom, "userIds": userList[i], "app_key": app_key,
                                     "timestamp": self.timestamp, "sign": sign}
                        # print('发送请求：'+str(self.data))
                        self.url = urlRemoveGroupUser
                        self.result = self.post()
                        try:
                            info = self.result.json()
                            print('移除组人员反馈： ', info)
                        except:
                            print(str(self.result))
                        print(info)
                        if info['code'] == 200:
                            print("从组里批量移除人员成功：" + str(len(userList[i])))

    def md5(self, input):
        input = input.encode('utf-8');
        md5sign = hashlib.md5()
        md5sign.update(input)
        md5value = md5sign.hexdigest()
        return md5value

    def trans_data_to_pair(self, data, index):
        contents = [
            data[i:i + index]
            for i in range(0, len(data), index)
        ]
        return contents


class EncryptJAVA(object):
    def __init__(self):
        if jpype.isJVMStarted():
            return
        jvmpath = jpype.getDefaultJVMPath()  # 获取默认的JVM路径
        print('默认的JVM路径为： %s'%jvmpath)
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
    '''此脚本实现把一个人员从所在组移动到另外一个组'''

    # host = '172.20.101.168'
    # groupFrom = 25
    # groupTO = 11
    # N = 1
    print("参数：base IP account password groupIDFrom groupIDTO N")
    # base=sys.argv[1]
    # host = sys.argv[2]
    # account = sys.argv[3]
    # password = sys.argv[4]
    # groupFrom = sys.argv[5]
    # groupTO = sys.argv[6]
    # N = sys.argv[7]

    # http
    base = 'http'
    # ip
    host = '10.9.244.113'
    #
    account = 'admin1234'
    password = 'admin1234'

    groupFrom = 95
    groupTO = 1
    N = 1

    obj = moveGroupUser(base, host, account, password, int(groupFrom), int(groupTO), int(N))
    obj.moveGroupUser()
