from BI_SenseEngine.ShareScripts.Command import Command
from BI_SenseEngine.ShareScripts.data_yaml import datagetConfig
import sys,time
windows_command = Command()
getConfig = datagetConfig()
#box = getConfig.getConfig().get("pic_comared_coordinate")
#getpath = str(sys.path[1]) + getConfig.getConfig().get("screen_path")
#closecommand = getConfig.getConfig().get("closecommand")#关闭上位机命令
#print(closecommand)
#windows_command.close_exe(closecommand)
#data_version = getConfig.getConfig().get('data_version')
#print(data_version)
#AT_command = getConfig.getConfig().get("AT_command")
chose_number = getConfig.getConfig().get("chose_number")  # 获取当前串口选择位置
star_times = getConfig.getConfig().get("star_times")  # 重启等待时长
print(star_times)
time.sleep(star_times)
print(1)
#print(AT_command)
#windows_command.close_exe('taskkill /IM %s /F' % "SenseEngineCameraV1.0.7.exe")
#print(sys.path[1])
