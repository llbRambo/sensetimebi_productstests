#!/bin/sh
audio_path=/data/audio_log.txt
sleep 10
i=1
while(true)
do
echo "-------------------------------it is $i time------------------------------------">>$audio_path
ubus call audio_recorder config '{"file": "/data/zql.aac"}'>>$audio_path
ubus call audio_recorder set_volume '{"volume":25}'>>$audio_path

ubus call audio_recorder start '{}'>>$audio_path
sleep 10
ubus call audio_recorder stop '{}'>>$audio_path
ubus call audio_player config '{"file": "/data/zql.aac"}'>>$audio_path
ubus call audio_player set_volume '{"volume":90}'>>$audio_path
ubus call audio_player start '{}'>>$audio_path
sleep 10
ubus call audio_player flush '{}'>>$audio_path
i=$(($i+1))
done
