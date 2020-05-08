#!/bin/sh
i=1
test_max=100000
while(true)
do	
	echo \n >>/data/log.txt
	echo "-----------------------------------------------This is the "$i" times!!------------------------------------------------------">>/data/log.txt
	echo "-----------------This is the "$i" times!!-----------------------">> /data/auth_result.txt
	date >> /data/auth_result.txt
	./test_sample_license >> /data/log.txt
	#echo $test
	i=$(($i+1))
	sleep 2
	if [ $i -eq $test_max ]
	then
		break
	fi
done
