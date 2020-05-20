#!/bin/sh
camera_path=/data/camera_log.txt
sleep 10
i=1
while(true)
do
echo "-------------------------------it is $i time------------------------------------">>$camera_path
ubus call camera open_camera '{"id":0}'>>$camera_path
sleep 1
ubus call camera start_preview '{"id":0}'>>$camera_path
sleep 30
ubus call camera stop_preview '{"id":0}'>>$camera_path
sleep 1
ubus call camera close_camera '{"id":0}'>>$camera_path
sleep 1
ubus call camera open_camera '{"id":1}'>>$camera_path
ubus call device.light set '{"id":11,"status":255}'>>$camera_path
sleep 1
ubus call camera start_preview '{"id":1}'>>$camera_path
sleep 30
ubus call camera stop_preview '{"id":1}'>>$camera_path
sleep 1
ubus call camera close_camera '{"id":1}'>>$camera_path
ubus call device.light set '{"id":11,"status":0}'>>$camera_path
sleep 1
i=$(($i+1))
done
      