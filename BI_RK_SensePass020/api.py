import requests
import json
import hashlib
import time

#login pw=账号+rsa加密之后的pw
#签名=时间戳+login的token+bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8

token = 'token-device-1:b233efca98514065bb06633775013178'
nowtime = lambda: int(round(time.time() * 1000))
timestamp = str(nowtime())


def get_sign():
    SECRET = 'bb635dd47e5861f717472df95652077356a8f38dea6347851c191f66b7cf9dc8'
    md5 = "AUTH-TIMESTAMP=" + timestamp + "&AUTH-TOKEN=" + token + "#" + SECRET
    m1 = hashlib.md5()
    m1.update(md5.encode("utf-8"))
    sign = m1.hexdigest()
    return sign


url = 'http://link-test.bi.sensetime.com'

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    'AUTH-TOKEN': token,
    'AUTH-TIMESTAMP': timestamp,
    'AUTH-SIGN': get_sign(),
    'LDID': 'SPS-cc8d61e43319262798afb06affea4f68'
}
postdata = \
    {
        "group_id": 243,
        "user_ids": [79601]
        # "type":"1",
        # "device_ids": [268]
        # "empty":0
    }
response = requests.post(url + "/sl/v2/groupuser", data=json.dumps(postdata), headers=headers)
print(response.text)