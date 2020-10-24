import os, re, time
import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=30,
#                  fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
                 fmt='[%(asctime)s][%(levelname)s]: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)

class Device_connect(object):
    def Command(self,command):
        process = os.popen(command)
        return process.read()

    def get_devices_state(self,sn):
        echo_divide = self.Command('adb devices').split('\n')
        size = len(echo_divide)
        if size > 1:
            for index in range(size-1):
                if echo_divide[index].find('\t') > -1:
                    end_pos =  echo_divide[index].index('\t')
                    name = echo_divide[index][:end_pos]
                    #print(name)
                    if name.find(sn)>-1:
                        state = echo_divide[index][end_pos:]
                        #print(name + " state is " + state)
                        return state

    def reconnect_device(self,sn):
        print("Recnnect device")
        self.Command('adb kill-server')
        self.Command('adb start-server')
        echo_info = self.Command('adb connect ' + sn)
        time.sleep(5)
        if echo_info.find("connected to " + sn) == 0:
            print('device 连接成功')
            return True
        else:
            print("连接失败")
            return False

    def reboot_device(self,sn):
        print("重启设备")
        self.Command("adb -s %s reboot"%sn)
        time.sleep(50)


    def check_device(self,sn):
        flag = True
        while flag:
            for j in range(30):
                time.sleep(1)
                if self.get_devices_state(sn).find("device") > -1:
                    print('device 连接成功')
                    flag = False
                    break
            if flag is False:
                continue
            #else:
                #print("重新连接")
               # self.reconnect_device(sn)
class getData(object):

    def Command(self,command):
        os.popen(command)

    def getTotalPss(self,ip):#获取内存
        lines = os.popen("adb -s %s shell dumpsys meminfo com.sensetime.demo "%ip).readlines() #逐行读取
        total = "TOTAL"
        for line in lines:
            if re.findall(total, line): # 找到TOTAL 这一行
                lis = line.split(" ")  #将这一行，按空格分割成一个list
                #print(lis)
                while '' in lis:       # 将list中的空元素删除
                    lis.remove('')
                return lis[1] #返回总共内存使用

    def getCpu(self,ip):#获取cpu
        li = os.popen("adb -s %s shell top -m 100 -n 1 -s cpu"%ip) .readlines()
        #adb shell dumpsys cpuinfo
        name = "com.sensetime.demo"
        #li = os.popen('adb shell "top -m 10 -n 1 -s cpu | grep com.sensetime.senseid5" ').readlines()

        for line in li:
            if re.findall(name,line):
                cuplist = line.split(" ")
                if cuplist[-1].strip() == 'com.sensetime.demo':
                    while '' in cuplist:       # 将list中的空元素删除
                        cuplist.remove('')
                    #print(cuplist)
                    return (cuplist[4])
                    #return float(cuplist[4].strip('%')) #去掉百分号，返回一个float

if __name__ == '__main__':

    getData = getData()
    devices = Device_connect()
    path = "D:\\test\\test_result\\log_"  + time.strftime('%m%d_%H%M%S') + '.txt'
    log = Logger(path, level='debug')
    log.logger.debug('内存-TOTAL,   CPU')
    device_sn ='10.9.40.33:8888'
    getData.Command('adb connect ' + device_sn)
    while True:
        try:
            #devices.check_device(device_sn)
            time.sleep(2)
            total = getData.getTotalPss(device_sn)
            cpu = getData.getCpu(device_sn)
            strlist = " %s,   %s"%(total,cpu)
            log.logger.debug(strlist)
        except:
            continue



'''
fig = plt.figure()
ax1 = fig.add_subplot(2,1,1,xlim=(0, 100), ylim=(0, 350))
ax2 = fig.add_subplot(2,1,2,xlim=(0, 100), ylim=(0, 100))
line, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
x = []
y= []
y2 = []
getData = getData()
def init():
    line.set_data([], [])
    line.set_data([], [])
    return line,line2
def getx():
    t = "0"
    return t

def animate(i):
    x.append(int(getx())+i)
    y.append(int(getData.getTotalPss())/1024) #每执行一次去获取一次值加入绘制的data中
    y2.append(getData.getCpu())
    print(x,y)
    line.set_data(x,y)
    line2.set_data(x,y2)
    return line,line2

anim1 = animation.FuncAnimation(fig, animate, init_func=init,  frames=1000, interval=30)
plt.show()
'''