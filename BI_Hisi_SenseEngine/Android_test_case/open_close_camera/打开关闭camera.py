#-- coding: utf-8 --
from M20_Android.pages import Device_pro

if __name__ == '__main__':
    ip = "10.9.66.2:8888"
    D = Device_pro(ip, "打开关闭camera")
    close_ir_camera_path = D.create_file("关闭IR预览界面截图") + "\\"
    close_rgb_camera_path = D.create_file("关闭RGB预览界面截图") + "\\"
    open_ir_camera_path = D.create_file("打开IR预览界面截图") + "\\"
    open_rgb_camera_path = D.create_file("打开rgb预览界面截图") + "\\"
    D.start_app()
    # D.check_Report_switch()
    D.into_preview()
    for i in range(187, 10000):
        close_ir_camera_name = "close_ir_%s.jpg"%i
        close_rgb_camera_name = "close_rgb_%s.jpg"%i
        open_ir_camera_name = "open_ir_%s.jpg"%i
        open_rgb_camera_name = "open_rgb_%s.jpg"%i

        D.onoff_camera(i,close_ir_camera_path,close_ir_camera_name,close_rgb_camera_path,close_rgb_camera_name
                       ,open_ir_camera_path,open_ir_camera_name,open_rgb_camera_path,open_rgb_camera_name)

        D.onoff_camera(i, close_ir_camera_path, close_ir_camera_name, close_rgb_camera_path, close_rgb_camera_name
                       , open_ir_camera_path, open_ir_camera_name, open_rgb_camera_path, open_rgb_camera_name)

