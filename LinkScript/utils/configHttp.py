# encoding: utf-8
import json
import os
import sys

import utils_funcs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # __file__获取执行文件相对路径，整行为取上一级的上一级目录
sys.path.append(BASE_DIR)  # 添加路径
import requests
import readConfig as readConfig
from utils.Log import MyLog

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.array = None
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: testintesr url
        :return:
        """
        if port != '':
            self.url = scheme + '://' + host + ':' + port + url
        else:
            self.url = scheme + '://' + host + url
        print(self.url)

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_array(self, array):
        """
        set params
        :param array:
        :return:
        """
        self.array = array

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, param, file_name):
        """
        set upload files
        :param param:
        :param file_name:
        :return:
        """
        if file_name != '':
            file_path = os.path.join(utils_funcs.testFile_path, 'images', file_name)
            f = open(file_path, "rb")
            self.files = {param: (str.split(file_path, "/")[-1], f, "image/jpeg")}

        if file_name == '' or file_name is None:
            self.state = 1
        return f

    def set_files1(self, files):
        """
        set upload files
        :return:
        """
        self.files = files

    def set_filesWithType(self, param, file_name, type):
        """
        set upload files
        :param filename:
        :return:
        """
        if file_name != '':
            # file_path = os.path.join(readConfig.proDir, "rsa.js")
            file_path = os.path.join(utils_funcs.testFile_path, 'file', file_name)
            f = open(file_path, "rb")
            self.files = {param: (str.split(file_path, "/")[-1], f, type)}

        if file_name == '' or file_name is None:
            self.state = 1
        return f

    def set_filesWithNullType(self, param, file_name):
        """
        set upload files
        :param filename:
        :return:
        """
        if file_name != '':
            # file_path = os.path.join(readConfig.proDir, "rsa.js")
            file_path = os.path.join(utils_funcs.testFile_path, 'file', file_name)
            f = open(file_path, "rb")
            self.files = {param: (str.split(file_path, "/")[-1], f)}
            print(self.files)

        if file_name == '' or file_name is None:
            self.state = 1
        return f

    # defined http get method
    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
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
                                     timeout=float(timeout), verify=False)
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, params=self.params, data=json.dumps(self.data),
                                     timeout=float(timeout), verify=False)
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
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
                                     timeout=float(timeout), verify=False)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout),
                                     verify=False)
            # print(self.data)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    def postWithArray(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.array, timeout=float(timeout),
                                     verify=False)
            # response.raise_for_status()

            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


if __name__ == "__main__":
    file = os.path.dirname(__file__)
    print(file)
