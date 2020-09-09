#!/usr/bin/python
# coding=utf-8
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
    # 打开rs485
    open_result = sk.socket_send(relay_open)
    print(relay_open, open_result)
    if open_result[0:2] == "OK":
        open = open + 1
    time.sleep(ON_TIME)
    # 发送rs485信号
    send_result = sk.socket_send(relay_send)
    print(relay_send, send_result)
    if send_result[0:2] == "OK":
        send = send + 1
    time.sleep(5)

    # 执行at+rs485=0的结果
    close_result = sk.socket_send(relay_close)
    print(relay_close, close_result)
    if close_result[12:28] == "3132333435363738":
        close = close + 1

    print(ip, "打开成功率为：", float(open) / i)
    print(ip, "发送成功率为：", float(send) / i)
    print(ip, "接收成功率为：", float(close) / i)
    print("--------------------------")
    sk.socket_close()
    return open, send, get_postback, close

def relay2_test(sk, send):
    # 发送rs485信号
    send_result = sk.socket_send(relay_send)
    print(relay_send, send_result)
    if send_result[0:2] == "OK":
        send = send + 1
    time.sleep(5)

    # 执行at+rs485=0的结果
    # close_result = sk.socket_send(at)
    # # print(relay_close, close_result)
    # if close_result[12:28] == "3132333435363738":
    #     print('数据回流成功')
    #     # close = close + 1
    print("发送成功率为：", float(send) / i)
    print("--------------------------")

    return  send


if __name__ == '__main__':
    iplist = '192.168.1.100'
    TEST_MAX = 50000
    ON_TIME = 1
    sock_port = 10000

    relay_open = "at+rs485=1\r\n"
    relay_send = "at+rs485=16,3132333435363738\r\n"
    relay_close = "at+rs485=0\r\n"
    at = "at\r\n"

    send_1 = 0

    sk = Socket(iplist, sock_port)
    sk.connect()
    # 打开rs485
    open_result = sk.socket_send(relay_open)
    # print(relay_open, open_result)
    # if open_result[0:2] == "OK":
    #     open = open + 1
    for i in range(1, TEST_MAX + 1):

        localtime = time.asctime(time.localtime(time.time()))
        print("------------------Test:", i, "-------------------")
        print("本地时间为 :", localtime)
        send_1 = relay2_test(sk, send_1)
    sk.socket_close()
