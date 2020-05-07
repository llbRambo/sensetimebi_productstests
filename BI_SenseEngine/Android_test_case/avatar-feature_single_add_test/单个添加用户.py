#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.40.167:8888"
    test_max = 20000
    D = Device_pro(ip,"单个添加用户")
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    D.delete_all()
    for i in range(1,test_max+1):
        D.log.logger.debug("----------test_%s----------" % i)
        user_name = "test_%s"%i
        D.add_an_user(user_name)