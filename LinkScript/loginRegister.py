# encoding: utf-8
import os
import sys
import time

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)  # 添加路径
import unittest
import readConfig as readConfig
from utils.Log import MyLog
from utils import common
from utils import configHttp
from utils.encryptUtils import encryptJAVA
from utils.encryptUtils import md5

localReadConfig = readConfig.ReadConfig()
configHttp = configHttp.ConfigHttp()
info = {}


class LoginRegister(unittest.TestCase):

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.case_name = "登录"
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")

    def testLoginRegister(self):
        """
        test body
        :return:
        """
        account = localReadConfig.get_account("account")
        password = localReadConfig.get_account("password")

        # total = 7
        typeList = ['SPS', 'SKP', 'SID', 'SPSP', 'SHL', 'SGBD', 'SPXS']
        # total=0
        self.success = 0
        self.fail = 0
        runtime = 10000

        print(str(runtime) + '次测试')

        for total in range(0, runtime):
            # set url
            # total+=1
            print('第' + str(total + 1) + '次登录')
            self.urlRsapub = common.get_url_from_xml('rsapub')
            self.urlLogin = common.get_url_from_xml('login')
            self.urlRegister = common.get_url_from_xml('registerV2')
            self.urlgroupDefault = common.get_url_from_xml('GroupDefaultV2')

            timestamp = int(time.time() * 1000)
            LANGUAGE = localReadConfig.get_headers("LANGUAGE")
            header = {"LANGUAGE": LANGUAGE}
            configHttp.set_headers(header)
            configHttp.set_url(self.urlRsapub)

            try:
                start = int(time.time() * 1000)
                self.return_json = configHttp.get()
                common.show_return_msg(self.return_json)
                self.info = self.return_json.json()
                end = int(time.time() * 1000)
                print('耗时' + str(end - start) + 'ms')
                if self.info['code'] == 200:
                    self.empoent = common.get_value_from_return_json(self.info, 'empoent')
                    self.module = common.get_value_from_return_json(self.info, 'module')
                    self.rsaId = common.get_value_from_return_json(self.info, 'rsa_id')

                    pw = encryptJAVA.encryptByRSA(self.empoent, self.module, password)

                    data = {"account": account, "password": pw, "rsa_id": self.rsaId, "identifier": typeList[0],
                            "duid": "device" + str(0)}
                    configHttp.set_data(data)
                    configHttp.set_url(self.urlLogin)
                    print(data)
                    try:
                        start = int(time.time() * 1000)
                        self.return_json = configHttp.postWithJson()
                        end = int(time.time() * 1000)
                        print('耗时' + str(end - start) + 'ms')
                        common.show_return_msg(self.return_json)
                        self.info = self.return_json.json()
                        if self.info['code'] == 200:
                            self.success = self.success + 1

                        else:
                            self.fail = self.fail + 1
                            continue
                    except Exception as err:
                        print(err)
                        self.fail = self.fail + 1
                        continue
                else:
                    self.fail = self.fail + 1
                    continue
            except Exception as err:
                print(err)
                self.fail = self.fail + 1
                continue

            print("当前成功：" + str(self.success))
            print("当前失败：" + str(self.fail))
        print("总共成功：" + str(self.success))
        print("总共失败：" + str(self.fail))

    def tearDown(self):
        """

        :return:
        """
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        print(self.return_json)
        common.show_return_msg(self.return_json)
        self.info = self.return_json.json()
        # show return message
        self.assertEqual(str(self.info['code']), "200")
        self.assertEqual(self.info['message'], 'OK')
