import serial,time,random
from sensetimebi_productstests.Sharedscript.SharedSerial import SerContrl
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay


if __name__ == '__main__':
    we_power_1 = SingleRelay(port="COM44", baudrate=9600) # 连接继电器
    we_powers = [we_power_1]
    print('we_power: %s'%we_powers)
    i = 6870
    testmax = 50001
    while i < testmax:
        print("——————test%s——————"%i)
        wait_times = we_power_1.wait_time()
        for we_power in we_powers:
            we_power.disconnect_power()  # 关闭电源
            print("第 %s 次断开"%i)
        randomtime1 = random.randrange(30,80)
        time.sleep(randomtime1)
        for we_power in we_powers:
            we_power.connect_power()  # 打开电源
            print("第 %s 次闭合"%i)
        randomtime2 = random.randrange(1, 5)
        time.sleep(randomtime2)
       #print("当前随机时间：%s,运行：%s次"%(wait_times,i))
        print("------------------------------")
        i += 1
