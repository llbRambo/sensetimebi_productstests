# encoding: utf-8
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import time
import readConfig as readConfig
import json
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from utils import configHttp
from utils.encryptUtils import md5
from utils.Log import MyLog

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = MyLog.get_log()
logger = log.get_logger()
caseNo = 0


def get_value_from_return_json(json, name1):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """
    info = json['data']
    value = info.get(name1)
    # value = group[name2]
    return value


def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址：" + url)
    # 可以显示中文
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name):
    """
    get testintesr data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


def get_workbook(xls_name):
    """
    get testintesr data from xls file
    :return:
    """
    #   cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    workbook = open_workbook(xlsPath)
    # get sheet by name
    # get one sheet's rows
    return workbook


def save_workbook(xls_name, workbook):
    """
    get testintesr data from xls file
    :return:
    """
    #   cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    workbook.save(xlsPath)
    return workbook


# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql


# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: testintesr's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in list(u):
                if c.text != "":
                    url_list.append(c.text)

    url = '/'.join(url_list)
    return url


def trans_data_to_pair(data, index):
    contents = []
    if len(data)>0:
        contents = [
            data[i:i + index]
            for i in range(0, len(data), index)
        ]
    # print(contents)
    return contents


def get_dict_value(in_dict, target_key, results=[], not_d=True):
    for key in in_dict.keys():  # 迭代当前的字典层级
        data = in_dict[key]  # 将当前字典层级的第一个元素的值赋值给data

        # 如果当前data属于dict类型, 进行回归
        if isinstance(data, dict):
            get_dict_value(data, target_key, results=results, not_d=not_d)
        if isinstance(data, list):
            for i in range(0, len(data)):
                get_dict_value(data[i], target_key, results=results, not_d=not_d)
        # 如果当前键与目标键相等, 并且判断是否要筛选
        if key == target_key and isinstance(data, dict) != not_d:
            results.append(in_dict[key])
    return results


def set_http_header(configHttp, token, ldid, LANGUAGE, SECRET):
    timestamp = int(time.time() * 1000)
    sign = md5("AUTH-TIMESTAMP=" + str(timestamp) + "&AUTH-TOKEN=" + token + "#" + SECRET)
    header = {"LANGUAGE": LANGUAGE, "AUTH-TIMESTAMP": str(timestamp), "AUTH-TOKEN": token, "LDID": ldid,
              "AUTH-SIGN": sign}
    print(header)
    configHttp.set_headers(header)


if __name__ == "__main__":
    # print(get_xls("login","login"))
    print(rootPath)
    # set_token_to_config()
