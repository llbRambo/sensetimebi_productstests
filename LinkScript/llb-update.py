# encoding: utf-8
import hashlib
import inspect
import os
import sys
import time

import jpype
import requests


def requestGet(url, headers, params):
    """
    defined get method
    :return:
    """
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        # response.raise_for_status()
        return response
    except TimeoutError:
        print("Time out!")
        return None

def postWithJson(url, headers, data):
    """
    defined post method
    :return:
    """
    try:
        response = requests.post(url, headers=headers, json=data, timeout=5, verify=False)
        # print(self.data)
        return response
    except TimeoutError:
        print("Time out!")
        return None

def getRsapub(scheme, host):
    '''
    获取Rsa密钥
    :return:
    '''
    urlRsapub = '%s://%s/sl/v2/rsapub'%(scheme, host)
    headers = {"LANGUAGE": 'LANGUAGE'}
    params = {}
    result = requestGet(urlRsapub, headers, params)
    try:
        info = result.json()
        print('获取密钥的反馈： ', info)
        if info['code'] == 200:
            print("获取Rsapub成功！")
            return info['data']['module'], info['data']['empoent'], info['data']['rsa_id']
    except:
        print(str(result))
        return


def register(headers):
    '''
    新设备注册
    :return:
    '''
    urlRegister = '%s://%s/sl/v2/device/register'%(scheme, host)  # 设备注册

    data = {
        "name": "1",
        "direction": 0
    }
    # data = {}
    result = postWithJson(urlRegister, headers, data)
    try:
        info = result.json()
        print('注册的反馈： ', info)
        if info['code'] == 200:
            print("设备注册成功！")
    except:
        print(str(result))
        return

def logIn(scheme, host, account, password):
    '''
    登录
    :return:
    '''
    urlLogin = '%s://%s/sl/v2/device/login'%(scheme, host)  # 设备登录
    module, empoent, rsaId = getRsapub(scheme, host)

    pw = encryptJAVA.encryptByRSA(empoent, module, password)
    data = {"account": account, "password": pw, "rsa_id": rsaId, "identifier": 'SPSE', "duid": ""}
    headers = ''
    # print(self.data)
    result = postWithJson(urlLogin, headers, data)
    try:
        info = result.json()
        print('登陆的反馈： ', info)
        if info['code'] == 200:
            # 使用返回的token，计算出header的token、sign
            SECRET = "bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8"
            timestamp = int(time.time() * 1000)
            token = info['data']['token']
            sign = md5("AUTH-TIMESTAMP=" + str(timestamp) + "&AUTH-TOKEN=" + token + "#" + SECRET)
            ldid = info['data']['device']['ldid']
            headers = {
                "LANGUAGE": 'zh',
                "AUTH-TIMESTAMP": str(timestamp),
                "AUTH-TOKEN": token,
                "AUTH-SIGN": sign,
                "LDID": ldid
            }

            if not info['data']['newDeviceKey']: #非新设备
                print("设备登录成功！")
            elif info['data']['newDeviceKey']: #新设备则进行注册
                register(headers)
            return headers
    except:
        print(str(result))
        return

def getAppKeyAndSecret(scheme, host, headers):
    '''
    获取app_key和app_secret
    :param feedbackinfo_login:
    :return:
    '''
    urlAppkey = '%s://%s/sl/v2/openapi/list'%(scheme, host)  # 获取openapi列表
    params = ''
    result = requestGet(urlAppkey, headers, params)
    try:
        info = result.json()
        print('获取openapi反馈： ', info)
        if info['code'] == 200:
            app_key = info['data'][0]['app_key']
            app_secret = info['data'][0]['app_secret']
            print("获取app_key和app_secret成功！")
            return app_key, app_secret
    except:
        print(str(result))
        return

def getAccountList(scheme, host, headers):
    '''
    获取用户列表
    :param scheme:
    :param host:
    :param headers:
    :return:
    '''
    urlGetAccountList = '%s://%s/sl/v2/account/list'%(scheme, host)
    params = ''
    result = requestGet(urlGetAccountList, headers, params)
    try:
        info = result.json()
        if info['code'] == 200:
            print('获取用户列表反馈：',info)
    except:
        print(str(result))
        return

def getAccount(scheme, host, headers):
    '''
    获取当前管理员信息
    :param scheme:
    :param host:
    :param headers:
    :return:
    '''

    urlGetAccount = '%s://%s/sl/v2/account'%(scheme, host)
    params = ''
    result = requestGet(urlGetAccount, headers, params)
    try:
        info = result.json()
        if info['code'] == 200:
            print('获取当前管理员信息反馈：', info)
    except:
        print(str(result))
        return


def deleteGroup(scheme, host, groupid, app_key, app_secret):
    urldeleteGroup = '%s://%s/api/v1/group/delete/%s'%(scheme, host, groupid)
    timestamp = int(time.time() * 1000)
    sign = md5(str(timestamp) + '#' + app_secret)
    headers = {"Referer": "http://10.9.244.113"}
    data = {
        "id": groupid,
        "sign": sign,
        "app_key": app_key,
        "timestamp": timestamp,
    }
    result = requestGet(urldeleteGroup, headers, data)
    try:
        info = result.json()
        print('删除指定人员组反馈： ', info)
        if info['code'] == 200:
            print('%s人员组删除成功',groupid)
    except:
        print(str(result))


def webconfig(scheme, host, headers, params):
    '''

    :param scheme:
    :param host:
    :param headers:
    :param deviceID:
    :param data:
    :return:
    '''
    urlwebconfigDevice = '%s://%s/sl/v2/device/update/server/config/batch' % (scheme, host)

    # params = {
    #     'id': deviceID,
    #     'group_staff': groupstaffList
    # }
    result = postWithJson(urlwebconfigDevice, headers, params)
    try:
        info = result.json()
        print('web参数配置：',info)
        if info['code'] == 200:
            print('更新成功！')
            print(info)
    except:
        print(str(result))


def updateDevice(scheme, host, headers, deviceID, groupstaffList):
    '''

    :param scheme:
    :param host:
    :param deviceID:
    :param groupList:
    :param app_key:
    :param app_secret:
    :return:
    '''
    urlupdateDevice = '%s://%s/sl/v2/device/update'%(scheme, host)

    params = {
        'id': deviceID,
        'group_staff': groupstaffList
    }
    result = postWithJson(urlupdateDevice, headers, params)
    try:
        info = result.json()
        if info['code'] == 200:
            print('更新成功！')
            print(info)
    except:
        print(str(result))




def md5(input):
    input = input.encode('utf-8')
    md5sign = hashlib.md5()
    md5sign.update(input)
    md5value = md5sign.hexdigest()
    return md5value

def trans_data_to_pair(data, index):
    contents = [
        data[i:i + index]
        for i in range(0, len(data), index)
    ]
    return contents


class EncryptJAVA(object):
    def __init__(self):
        cur_file_path = inspect.getfile(inspect.currentframe())  # 得到定义该函数的脚本路径
        path = os.path.abspath(os.path.dirname(cur_file_path))
        if jpype.isJVMStarted():
            return
        jvmpath = jpype.getDefaultJVMPath()  # 获取默认的JVM路径
        print('默认的JVM路径为： %s'%jvmpath)

        jarPath = os.path.join(path, "jar", "encryptUtils.jar")
        dependency = os.path.join(path, "jar", 'dependency')
        print('path：', path)
        print('jarPath：', jarPath)
        print('dependency：', dependency)
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
        '''
        关闭JVM
        :return:
        '''
        jpype.shutdownJVM()

encryptJAVA = EncryptJAVA()

if __name__ == '__main__':
    scheme = 'http'
    host = '10.9.244.113'
    account = 'admin1234'
    passws = 'admin1234'
    deviceID = 1004
    groupstaffList1 = [6, 7]
    groupstaffList2 = [6, 7]
    groupstaffList3 = [6, 7, 8]

    headers = logIn(scheme, host, account, passws)
    a, b = getAppKeyAndSecret(scheme, host, headers)
    # deleteGroup(scheme, host, '136', a, b)
    # getAccount(scheme, host, headers)
    # updateDevice(scheme, host, headers, deviceID, groupstaffList1)
    #
    # for i in range(1, 2):
    #     t = time.strftime('%Y/%m/%d %H:%M:%S')
    #     print('__________[%s]%s__________'%(str(t),i))
    #     updateDevice(scheme, host, headers, deviceID, groupstaffList1)
    #     time.sleep(10 * 60)
    #     updateDevice(scheme, host, headers, deviceID, groupstaffList2)
    #     time.sleep(10 * 60)
    #     updateDevice(scheme, host, headers, deviceID, groupstaffList3)
    #     time.sleep(10 * 60)
    # vatime = 27
    # reboottime = '16:27:00'
    # print(reboottime)
    # postdata14 = {
    #     "deviceIds": [558],
    #     "sps": {
    #         "reboot_time":reboottime
    #     }
    # }
    # postdata15 = {
    #     "deviceIds": [1004],
    #     "sps": {
    #         "reboot_time": reboottime
    #     }
    # }
    webconfig(scheme, host, headers, postdata14)
    webconfig(scheme, host, headers, postdata15)