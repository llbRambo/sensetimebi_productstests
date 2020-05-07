#-- coding: utf-8 --
from M20_Android.pages import Device_pro


if __name__ == '__main__':
    ip = "10.9.40.110:8888"
    test_max = 20000
    D = Device_pro(ip,"暂停恢复识别")
    pause_img_path = D.create_file("暂停识别截图")+"\\"
    resetore_img_path =D.create_file("恢复识别截图")+"\\"
    D.start_app()
    D.check_Report_switch()
    D.into_preview()
    for i in range(1,test_max+1):
        pause_name = "pause_img_%s.jpg"%i
        resetore_name = "resetore_img_%s.jpg"%i
        D.recognition(pause_img_path,pause_name,resetore_img_path,resetore_name,i)

    D.stop_app()