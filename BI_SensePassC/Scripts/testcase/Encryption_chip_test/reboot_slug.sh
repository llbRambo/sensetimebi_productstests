#!/bin/sh
sleep 40
line=$(tail -n -1 /data/reboot_num.txt)
test_max=4
i=1
echo "################################################This is the "$line" times Reboot!!#####################################################">>/data/reboot_slug.txt
echo "########################This is the "$line" times Reboot!!###########################">> /auth_result.txt
while(true)
do	
	echo \n >>/data/reboot_slug.txt
	echo "------------------------------------------This is the "$i" times!!-------------------------------------------------">>/data/reboot_slug.txt
	echo "--------------This is the "$i" times!!------------------">> /auth_result.txt
	date >> /auth_result.txt
	./data/test_sample_license >> /data/reboot_slug.txt
	#echo $test
	i=$(($i+1))
	sleep 2
	if [ $i -eq $test_max ]
	then
		break
	fi
done
time=$(($line+1))
echo $time >> /data/reboot_num.txt
sleep 5
reboot -f


 
