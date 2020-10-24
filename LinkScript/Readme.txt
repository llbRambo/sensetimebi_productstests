环境需要：1.如未安装jpype，需安装依赖库pip install jpype1。如安装报错，自行百度或参考：https://blog.csdn.net/shuihupo/article/details/79714949
        2.安装Java环境，自行百度
脚本说明：
addBlackLink.py: 添加黑名单人员
    参数6个：url前缀（http or https） IP/域名 账号 密码 黑名单组ID 图片路径地址
    运行示例：python addBlackLink.py https link-test.bi.sensetime.com xiaoliping Admin1234 3 添加人员的具体图片路径

updateGroupUser.py: 将已存在的user添加进组里
    参数7个：url前缀（http or https） IP/域名 账号 密码 组ID 人员ID-start 人员ID-end
    运行示例：python updateGroupUser.py https link-test.bi.sensetime.com xiaoliping Admin1234 3 添加人员的具体图片路径

addUserLink.py: 添加人员--非强制，如库中已存在相似人员，则该人员添加失败
    参数6个：url前缀（http or https） IP/域名 账号 密码 人员组ID 图片路径地址
    运行示例：python addUserLink.py https link-test.bi.sensetime.com xiaoliping Admin1234 3 添加人员的具体图片路径

addUserLinkForce.py: 添加人员--强制，如库中已存在相似人员，则该人员依旧可添加成功
    参数6个：url前缀（http or https） IP/域名 账号 密码 人员组ID 图片路径地址
    运行示例：python addUserLinkForce.py https link-test.bi.sensetime.com xiaoliping Admin1234 3 添加人员的具体图片路径

deleteBlackLink.py: 批量删除黑名单人员
    参数7个：url前缀（http or https） IP/域名 账号 密码  黑名单人员ID-start 黑名单人员ID-end  需删除的黑名单总数
    运行示例：python deleteBlackLink.py https link-test.bi.sensetime.com xiaoliping Admin1234 1 1000 500

deleteUserLink.py: 批量删除人员
    参数7个：url前缀（http or https） IP/域名 账号 密码  人员ID-start 人员ID-end  需删除的人员总数
    运行示例：python deleteUserLink.py https link-test.bi.sensetime.com xiaoliping Admin1234 1 1000 500

batchMoveGroupUser.py: 从某个组批量移动人员至另一个组
    参数7个：url前缀（http or https） IP/域名 账号 密码  组ID-From 组ID-To  需移动的人员总数
    运行示例：python batchMoveGroupUser.py https link-test.bi.sensetime.com xiaoliping Admin1234 1 5 50

qrcodeContent.py: 生成某个人员的通行二维码
    参数6个：url前缀（http or https） IP/域名 账号 密码  人员ID 通行次数
    运行示例：python qrcodeContent.py https link-test.bi.sensetime.com xiaoliping Admin1234 1 2

testWebSocket.py: 获取识别记录的推送（私有部署）
    参数4个：url前缀（http or https） IP/域名 账号 密码
    运行示例：python testWebSocket.py http 172.20.101.168 xiaoliping Admin1234




