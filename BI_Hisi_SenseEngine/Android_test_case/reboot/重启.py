#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.40.22:8888"
    test_max = 2000
    D = Device_pro(ip,"重启设备")
    reboot_path =D.create_file("重启后打开预览界面截图")+"\\"
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    for i in range(1,test_max+1):
        reboot_name = "reboot_%s.jpg"%i
        D.reboot_system(i,reboot_path,reboot_name)
