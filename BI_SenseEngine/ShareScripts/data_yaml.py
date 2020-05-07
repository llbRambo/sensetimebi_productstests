import os,yaml, sys

class datagetConfig(object):
    def getConfig(self, yamlname):
        # 获取被执行脚本所在文件夹路径
        # curPath = os.path.dirname(os.path.realpath(__file__))
        curPath_str = str(sys.path[0])
        # 获取yaml文件路径
        yamlname_str = str(yamlname)
        yamlPath = os.path.join(curPath_str, yamlname_str)
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        return yaml.load(cfg, Loader=yaml.FullLoader)  # 用load方法转字典
