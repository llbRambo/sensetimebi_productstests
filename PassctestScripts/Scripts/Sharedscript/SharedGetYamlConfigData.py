import os
import sys
import yaml


class DataGetConfig(object):
    def getConfig(self, yamlname):
        # 获取当前脚本所在文件夹路径
        curPath = str(sys.path[0])
        #print(curPath)
        # 获取yaml文件路径
        yamlname_str = str(yamlname)
        yamlPath = os.path.join(curPath, yamlname_str)
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        return yaml.load(cfg, Loader=yaml.FullLoader)  # 用load方法转字典
