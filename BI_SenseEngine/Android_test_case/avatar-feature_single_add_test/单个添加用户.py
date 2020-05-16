#-- coding: utf-8 --
from sensetimebi_productstests.BI_SenseEngine.Android_test_case.AndroidShareScripts.pages import SenseEngineCameraDemoDebugApk
if __name__ == '__main__':
    ip = "10.9.40.51:8888"
    test_max = 20000
    D = SenseEngineCameraDemoDebugApk(ip, "单个添加用户")
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    D.delete_all()
    for i in range(9811, test_max+1):
        D.log.logger.debug("----------test_%s----------" % i)
        D.add_an_user(str(i))