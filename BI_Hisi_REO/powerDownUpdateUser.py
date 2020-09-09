import time
from sensetimebi_productstests.Sharedscript.SharedSerial import SingleRelay
from sensetimebi_productstests.LinkScript.moveGroupUsersUpdate import moveGroupUser
from sensetimebi_productstests.Sharedscript.SharedSerial import SerContrl



if __name__ == '__main__':
    # http
    base = 'http'
    # ip
    host = '10.9.244.113'
    #
    account = 'admin1234'
    password = 'admin1234'

    groupFrom = 95
    groupTO = 1
    N = 5

    destinationGroup = 96
    sourceGroup = 95
    id = 119050

    obj = moveGroupUser(base, host, account, password, int(groupFrom), int(groupTO), int(N))


    for i in range(1,10001):
        print('————————test No.%s————————'%i)
        # ser_relay = SingleRelay('com33', 9600)
        # ser = SerContrl('com21', 115200)
        # 将某一人员移出某个组
        obj.singleMoveGroupUser(destinationGroup, sourceGroup, id)  # 移出人员
        # 刷脸
        # 掉电
        #ser_relay.disconnect_power()
        time.sleep(10)
        # 将移出的人员再次添加进组内
        obj.singleMoveGroupUser(sourceGroup, destinationGroup, id)  # 添加人员
        # 刷脸
        # 查询特征值，与备份的原始特征值对比
        # ser.send_cmd("source /etc/profile; ubus call ai ai_db_get_feature '{\"id\":\"119050\"}'")
        # info = ser.read_data()
        # print(info)
        # 刷脸
        # 上电
        #ser_relay.connect_power()
        # 查询特征值，与备份的原始特征值对比
        time.sleep(10)