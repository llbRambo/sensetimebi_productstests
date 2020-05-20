#!/usr/bin/python
#coding=utf-8
import os
import sys
import time
import datetime
import autoit
from sensetimebi_productstests.Sharedscript.SharedSOCKET import Socket

def relay_test(ip, port, open, send, get_postback, close):
    print(ip)        
    sk = Socket(ip, port)
    sk.connect()
    #打开rs485
    open_result = sk.socket_send(relay_open)
    print(relay_open, open_result)
    if open_result[0:2] == "OK":
        open = open + 1
    time.sleep(ON_TIME)
    #发送rs485信号
    send_result = sk.socket_send(relay_send)
    print(relay_send, send_result)
    if send_result[0:2] == "OK":
        send = send + 1
    time.sleep(5)

    #执行at+rs485=0的结果
    close_result = sk.socket_send(relay_close)
    print(relay_close, close_result)
    if close_result[12:28] == "3132333435363738":
        close = close + 1

    print(ip, "打开成功率为：", float(open)/i)
    print(ip, "发送成功率为：", float(send)/i)
    print(ip, "接收成功率为：", float(close)/i)
    print("--------------------------")
    sk.socket_close()
    return open, send, get_postback, close
        

if __name__ == '__main__':
    #在指定路径下打开RS485Check_sensepassX.exe
    a = autoit.run('D:\\test-project\\000-testScripts\\sensetimebi_productstests\\BI_SensePassC\\testTools\\RS485Check_sensepassX\\RS485Check_sensepassX')
    print(a)
    time.sleep(2)
    autoit.mouse_click(button='left', x=1130, y=457, clicks=1, speed=-1) #
    time.sleep(2)
    autoit.mouse_click(button='left', x=1130, y=517, clicks=1, speed=-1) #选中485串口号
    time.sleep(2)
    autoit.mouse_click(button='left', x=845, y=620, clicks=1, speed=-1) #点击开始
    time.sleep(2)
    #打开之后选中485串口

    #
    # iplist = ['192.168.1.110']
    # TEST_MAX = 3
    # ON_TIME = 1
    # sock_port = 10000
    #
    # relay_open = "at+rs485=1\r\n"
    # relay_send = "at+rs485=16,3132333435363738\r\n"
    # relay_close = "at+rs485=0\r\n"
    # open_1 = 0
    # send_1 = 0
    # get_postback1 = 0
    # close_1 = 0
    # open_2 = 0
    # send_2 = 0
    # get_postback2 = 0
    # close_2 = 0
    # open_3 = 0
    # send_3 = 0
    # get_postback3 = 0
    # close_3 = 0
    #
    # for i in range(1, TEST_MAX+1):
    #
    #     localtime = time.asctime(time.localtime(time.time()))
    #     print("------------------Test:", i, "-------------------")
    #     print("本地时间为 :", localtime)
    #
    #     for ip in iplist:
    #         try:
    #             if ip == '192.168.1.110':
    #                 open_1, send_1, get_postback1, close_1 = relay_test(ip, sock_port, open_1, send_1, get_postback1, close_1)
    #             elif ip == '192.168.1.100':
    #                 open_2, send_2, get_postback2, close_2 = relay_test(ip, sock_port, open_2, send_2, get_postback2, close_2)
    #             elif ip == '192.168.1.101':
    #                 open_3, send_3, get_postback3, close_3 = relay_test(ip, sock_port, open_3, send_3, get_postback3, close_3)
    #         except:
    #             continue
