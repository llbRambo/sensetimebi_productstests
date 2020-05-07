#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.40.110:8888"
    test_max = 2000
    D = Device_pro(ip,"升级固件")
    upload_fail_paths = D.create_file("升级固件失败截图")+"\\"
    start_path =D.create_file("升级后打开预览界面截图")+"\\"
    for i in range(1,test_max+1):
        D.start_app()
        D.check_Report_switch()
        D.into_preview()
        start_name = "start_%s.jpg"%i
        D.screen_img(start_path,start_name)
        upload_name = "upload_%s.jpg"%i
        D.bin_upgrade(i,upload_fail_paths,upload_name)