#!/user/bin/python
#coding=utf-8
import os
import sys
import time
import datetime
import sys
import socket

#TCP = SOCK_STREAM
#UDP = socket.SOCK_DGRAM
ip = '192.168.1.100'
#iplist = ['192.168.1.108']
port = 10000

TEST_MAX = 10000
ON_TIME = 0.5

relay_open = "AT+RELay=0,1\r\n"
relay_close = "AT+RELay=0,0\r\n"
# Demo
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    #创建一个socket 
sock.connect((ip,port))

for i in range(1, TEST_MAX+1):
    localtime = time.asctime( time.localtime(time.time()) )
    print ("------------------Test:",i ,"-------------------")
    print ("本地时间为 :", localtime)
   
    print(ip)        #print('\r\n')
    print (relay_open)
    sock.send(relay_open.encode())
    print ("relay_open:",(sock.recv(1024).decode('utf-8')))
    time.sleep(ON_TIME)
    print(relay_close)
    sock.send(relay_close.encode())
    print("relay_close:", (sock.recv(1024).decode('utf-8')))
    time.sleep(ON_TIME)
sock.close()

