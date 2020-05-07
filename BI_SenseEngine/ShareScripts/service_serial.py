import serial,time,binascii,random
class M20_serial(object):
    def __init__(self,port,baudrate):

        # 打开端口
        self.port = serial.Serial(port=port, baudrate=baudrate,timeout=2)

    # 发送指令的完整流程
    def send_cmd(self, AT):
        self.port.write(AT)
        time.sleep(0.02)

    # 读取当前串口信息
    def read_all(self):
        response = self.port.read_all()
        response = response.decode()
        strlists = response.splitlines()
        return strlists

    #关闭串口
    def port_close(self):
        self.port.close()
    #打开串口
    def port_open(self):
        self.port.open()

    # 文档输入编码转译
    def asc_str(self,common):
        atstrlist = []
        strings = common + '\r\n'
        for string in strings:
            string2 = bytes(string, encoding='utf-8')
            string_int2 = int(binascii.b2a_hex(string2), 16)
            atstrlist.append(string_int2)
        return bytes(atstrlist)

    #  读取文档串口输入
    def read_value(self,filename):
        #filename = 'string.txt'
        atlist = []
        with open(filename, 'r')as file_to_read:
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                lines = lines[0:-1]
                if not lines:
                    break
                    pass
                # p_tmp = [str(i) for i in lines.split("\n")]
                atlist.append(lines)
            #print(atlist)
            return atlist

    # 文档输入编码转译
    def asc_strlist(self,filename):
        atlist = self.read_value(filename)
        atlists = []
        for strings in atlist:
            stringlist = self.asc_str(strings)
            #print(strings, stringlist)
            atlists.append(stringlist)
        return atlists

    def Query_version(self):
        ATVER = self.asc_str("AT+VER")
        enter = self.asc_str("")
        self.send_cmd(enter)
        self.send_cmd(ATVER)
        time.sleep(3)
        strlists = self.read_all()
        return strlists

    def connect_power(self):
        connect = bytes([160, 1, 0, 161])  # A0 01 00 A1       上电
        connect_1 = bytes([160, 2, 0, 162])  # A0 02 00 A2       第二路上电
        self.send_cmd(connect)
        self.send_cmd(connect_1)

    def disconnect_power(self):
        disconnect = bytes([160, 1, 1, 162])  # A0 01 01 A2    断电
        disconnect_1 = bytes([160, 2, 1, 163])  # A0 02 01 A3    第二路断电
        self.send_cmd(disconnect)
        self.send_cmd(disconnect_1)

    def power_operation(self):
        self.disconnect_power()
        time.sleep(1)
        self.connect_power()

    def switch_time(self):
        return(random.randint(80,100))

if __name__ == '__main__':
    ms = M20_serial(port="COM10",baudrate=9600)
    ms.disconnect_power()
    ms.power_operation()



