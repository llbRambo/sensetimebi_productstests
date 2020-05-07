#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.40.110:8888"
    test_max = 20000
    D = Device_pro(ip,"单个添加特征值")
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    D.add_an_user("test")
    D.get_feature("test")
    for i in range(1,test_max+1):
        D.add_feature("test_%s"%i)
        D.log.logger.debug("----------test_%s----------"%i)