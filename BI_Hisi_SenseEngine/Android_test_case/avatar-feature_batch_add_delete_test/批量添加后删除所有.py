#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.40.116:8888"
    test_max = 2000
    D = Device_pro(ip,"批量添加后删除所有")
    add_fail_path =D.create_file("添加失败截图")+"\\"
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    D.delete_all()
    for i in range(1,test_max+1):
        D.log.logger.debug("----------test_%s----------"%i)
        add_name = "add_%s.jpg"%i
        D.add_batch_user(add_fail_path,add_name)
        D.delete_all()
