#!/user/bin/python
#coding=utf-8
import os
import sys
import time
import datetime
import sys
import socket
import sys
origin = sys.stdout
def get_median_1(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

def choose(s):
    #sum = 0
   # all = 0
    maxnum = max(s)
    minnum = min(s)
  #  for i in s:
 #       sum = sum + 1 #元素个数
#        all = all + i
#    average = all / sum
    print(maxnum)
    print(minnum)


#TCP = SOCK_STREAM
#UDP = socket.SOCK_DGRAM
ip = '192.168.1.100'
iplist = ['192.168.1.100']
port = 10000

TEST_MAX = 1
ON_TIME = 10
num= []
psensor_on = "AT+ PSENSOR=1\r\n"
psensor_off = "AT+ PSENSOR=0\r\n"
bodydetect = "AT+BODYDETECT=1\r\n"
       #print('\r\n')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建一个socket 
sock.connect((ip,port))
print(ip)
print (bodydetect)
sock.send(bodydetect.encode())
print ("bodydetect:",(sock.recv(1024).decode('utf-8')))

for i in range(1, TEST_MAX+1):
    localtime = time.asctime( time.localtime(time.time()) )
    print ("------------------Test:",i ,"-------------------")
    print ("本地时间为 :", localtime)
    print (psensor_on)
    sock.send(psensor_on.encode())
    #time.sleep(ON_TIME)
    print ("psensor_on:",(sock.recv(1024).decode('utf-8')))
    time.sleep(ON_TIME)
    #print (psensor_off)
    #sock.send(psensor_off.encode())
    result = sock.recv(1024).decode('utf-8')
    list = result.split("\n")
    
    for l in list:
        #print(len)
        try:
            l = l.split(" ")
            print(int(l[2]))
            num.append(int(l[2]))
        except:
            pass
with open('D:/0306.txt', 'w') as f:
    sys.stdout = f
    for j in num:
        print(j)
    #median = get_median_1(num)
    #print("中位数:"+str(median))
    #print(median)
    #choose(num)
    sys.stdout = origin
  

