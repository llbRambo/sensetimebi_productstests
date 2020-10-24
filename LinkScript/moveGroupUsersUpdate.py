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
        self.LANGUAGE = 'zh'
        self.ldid = ''
        self.sign = ''
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

    def getRsapub(self):
        '''
        获取Rsa密钥
        :return:
        '''
        urlRsapub = self.scheme + "://" + self.host + '/sl/v2/rsapub'  # RSA密钥获取

        self.headers = {"LANGUAGE": self.LANGUAGE}
        self.url = urlRsapub
        self.result = self.get()
        try:
            info = self.result.json()
            print('获取密钥的反馈： ', info)
            if info['code'] == 200:
                print("获取Rsapub成功！")
                return info
        except:
            print(str(self.result))
            return

    def logIn(self, feedbackinfo_getrsapub):
        '''
        登录
        :return:
        '''
        urlLogin = self.scheme + "://" + self.host + '/sl/v2/device/login'  # 设备登录
        empoent = feedbackinfo_getrsapub['data']['empoent']
        module = feedbackinfo_getrsapub['data']['module']
        rsaId = feedbackinfo_getrsapub['data']['rsa_id']
        pw = encryptJAVA.encryptByRSA(empoent, module, self.password)
        self.data = {"account": self.account, "password": pw, "rsa_id": rsaId, "identifier": 'SPS', "duid": "1"}
        self.url = urlLogin
        # print(self.data)
        self.result = self.postWithJson()
        try:
            info = self.result.json()
            print('登陆的反馈： ', info)
            if info['code'] == 200:
                print("设备登录成功！")
                return info
        except:
            print(str(self.result))
            return

    def register(self, feedbackinfo_login):
        '''
        新设备注册
        :return:
        '''
        urlRegister = self.scheme + "://" + self.host + '/sl/v2/device/register'  # 设备注册
        token = feedbackinfo_login['data']['token']
        self.ldid = feedbackinfo_login['data']['device']['ldid']
        if feedbackinfo_login['data']['newDeviceKey']:
            self.sign = self.md5(
                "AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
            self.headers = {"LANGUAGE": self.LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                            "LDID": self.ldid,
                            "AUTH-SIGN": self.sign}
            self.data = {"name": "1", "direction": 2, "location": "xlplocation_",
                         "description": "description", "software_version": "v2.2.2", "info": "info"}
            self.url = urlRegister
            self.result = self.postWithJson()
            try:
                info = self.result.json()
                print('注册的反馈： ', info)
                if info['code'] == 200:
                    print("设备注册成功！")
            except:
                print(str(self.result))
                return

    def getAppKeyAndSecret(self, feedbackinfo_login):
        '''
        获取app_key和app_secret
        :param feedbackinfo_login:
        :return:
        '''
        urlAppkey = self.scheme + "://" + self.host + '/sl/v2/openapi/list'  # 获取openapi列表
        token = feedbackinfo_login['data']['token']  #获取token
        self.sign = self.md5("AUTH-TIMESTAMP=" + str(self.timestamp) + "&AUTH-TOKEN=" + token + "#" + self.SECRET)
        self.headers = {"LANGUAGE": self.LANGUAGE, "AUTH-TIMESTAMP": str(self.timestamp), "AUTH-TOKEN": token,
                        "LDID": self.ldid, "AUTH-SIGN": self.sign}
        self.url = urlAppkey
        self.result = self.get()
        try:
            info = self.result.json()
            print('获取openapi反馈： ', info)
            if info['code'] == 200:
                app_key = info['data'][0]['app_key']
                app_secret = info['data'][0]['app_secret']
                print("获取app_key和app_secret成功！")
                return app_key, app_secret
        except:
            print(str(self.result))
            return

    def updateGroupUser(self, url, app_key, app_secret, groupid, userid):
        '''
        更新人员组里的人员
        :param app_key:
        :param app_scert:
        :return:
        '''

        # 往组里添加人员
        self.timestamp = int(time.time() * 1000)  #时间戳处理
        self.headers = {"Referer": "http://www.sensetime.com"}
        self.sign = self.md5(str(self.timestamp) + '#' + app_secret)  #签名
        self.data = {"groupId": groupid, "userIds": userid, "app_key": app_key,
                     "timestamp": self.timestamp, "sign": self.sign}
        # print('发送请求：'+str(self.data))
        self.url = url
        self.result = self.post()
        try:
            info = self.result.json()
            print('更新组人员反馈： ', info)
            if info['code'] == 200:
                print("批量添加人员到组成功:" + str(userid))
        except:
            print(str(self.result))

    def singleMoveGroupUser(self, destinationGroup, sourceGroup, userid):
        urlAddGroupUser = self.scheme + "://" + self.host + '/api/v1/user/add/group'  # 添加人员到组
        urlRemoveGroupUser = self.scheme + "://" + self.host + '/api/v1/user/remove/group'  # 从组中移出人员

        feedbackinfo_getrsapub = self.getRsapub()  # 获取Rsa密钥
        feedbackinfo_login = self.logIn(feedbackinfo_getrsapub)  # 登录
        self.register(feedbackinfo_login)  # 新设备注册
        app_key, app_secret = self.getAppKeyAndSecret(feedbackinfo_login)  # 获取app_key和app_secret

        self.updateGroupUser(urlAddGroupUser, app_key, app_secret, destinationGroup, userid)  # 把员工移动到另外一个组
        self.updateGroupUser(urlRemoveGroupUser, app_key, app_secret, sourceGroup, userid)  # 把移动了员工在本组删除

    def batchMoveGroupUser(self):
        """
        test body
        :return:
        """

        # set url
        urlGroupUser = self.scheme+"://" + self.host + '/sl/v2/group/sync'  #获取组内所有用户ID
        urlAddGroupUser = self.scheme + "://" + self.host + '/api/v1/user/add/group'  # 添加人员到组
        urlRemoveGroupUser = self.scheme + "://" + self.host + '/api/v1/user/remove/group'  # 从组中移出人员

        feedbackinfo_getrsapub = self.getRsapub()  #获取Rsa密钥
        feedbackinfo_login = self.logIn(feedbackinfo_getrsapub)  #登录
        self.register(feedbackinfo_login) #新设备注册
        app_key,app_secret = self.getAppKeyAndSecret(feedbackinfo_login) #获取app_key和app_secret

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
            self.updateGroupUser(urlAddGroupUser, app_key, app_secret, self.groupTo, userList[i])
            self.updateGroupUser(urlRemoveGroupUser, app_key, app_secret, self.groupFrom, userList[i])


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
    N = 5

    destinationGroup = 96
    sourceGroup = 95
    id = 119050

    obj = moveGroupUser(base, host, account, password, int(groupFrom), int(groupTO), int(N))
    # obj.batchMoveGroupUser() # 批量移动人员
    obj.singleMoveGroupUser(destinationGroup, sourceGroup, id)  # 移出人员
    # obj.singleMoveGroupUser(sourceGroup, destinationGroup, id)  # 添加人员
