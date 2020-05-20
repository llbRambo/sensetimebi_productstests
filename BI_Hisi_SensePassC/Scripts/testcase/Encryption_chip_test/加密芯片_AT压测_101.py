import socket
import datetime
import xlsxwriter
import time
sn_workbook = xlsxwriter.Workbook('d:\加密芯片sn_1.xlsx')
sn_worksheet = sn_workbook.add_worksheet()

otp_workbook = xlsxwriter.Workbook('d:\加密芯片otp_1.xlsx')
otp_worksheet = otp_workbook.add_worksheet()

#TCP = SOCK_STREAM
#UDP = socket.SOCK_DGRAM
#iplist = ['192.168.1.101','192.168.1.103','192.168.1.104','192.168.1.105','192.168.1.106','192.168.1.107','192.168.1.108']
iplist = ["192.168.1.100"]
port = 10000
TEST_MAX = 90000

slug_cmd_sn = "AT+ATSHA204A\r\n"
slug_cmd_otp = "AT+otp\r\n"
sn_count = 0
otp_count = 0
sn_list = []
otp_list = []
s_list = []
sn = "0123678133F93BC6EE"  #每台设备不一样需要
otp = "SensePass C"
for i in range(1, TEST_MAX+1):
    date = datetime.datetime.now()
    print("-------------------- Test "+ str(i) +"---------------------------------")
    print(date)
    for ip in iplist:
        print(ip)
       
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建一个socket
        sock.connect((ip,port))
        print(slug_cmd_sn)
        sock.send(slug_cmd_sn.encode())
        result = sock.recv(1024).decode('utf-8')
        print(result)
        r=result.split("\n")
        s_result = r[0].split(": ")[1].strip()
        sn_result = s_result[0:]
        if sn_result == "7":
            print("加密芯片sn号读取失败")    
        elif sn_result == sn:
            sn_count = sn_count + 1
        else:
            print("加密芯片sn号读取错误")
            sn_list.append(sn_result)
            
        print(slug_cmd_otp)
        sock.send(slug_cmd_otp.encode())
        result = sock.recv(1024).decode('utf-8')
        print(result)
        r=result.split("\n")
        o_result = r[0].split(": ")[1].strip()
        otp_result = o_result[0:]
        if otp_result == "7":
            print("加密芯片otp号读取失败")
        elif otp_result == otp :
            otp_count = otp_count + 1
        else:
            print("加密芯片otp号读取错误")
            otp_list.append(otp_result)
        print("---------------------")
        sock.close()
        
sn_per = float(sn_count)/TEST_MAX
otp_per = float(otp_count)/TEST_MAX
print("AT+ATSHA204成功次数为："+str(sn_count))
print("AT+otp成功次数为："+str(otp_count))

print("AT+ATSHA204成功率为 :" + str(sn_per))
print("AT+otp成功率为 :" + str(otp_per))

i = 0
j = 0
for sn in sn_list:
    sn_worksheet.write(i,0,sn)
    i = i+1
for otp in otp_list:
    otp_worksheet.write(j,1,otp)
    j = j+1
sn_workbook.close()
otp_workbook.close()
       
