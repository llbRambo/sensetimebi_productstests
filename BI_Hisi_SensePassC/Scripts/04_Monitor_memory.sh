#!/bin/sh
path=/data/memory
if [ ! -d $path ];then
	mkdir -p "$path"
else
	echo "目录已经存在"
fi
rm /data/memory/*.txt
rm /data/memlog.txt
i=1
logpath=/data/memlog.txt
App=/usr/bin/sensepassx-app
while [ $i -lt 400 ]
do
{
	echo "------------------It is "$i" times " $(date)"----------------------">>$logpath
	#date >> /data/memlog.txt
	for proc in app device_service ai_service camera_service fota_service media_service sensor_service
		do
			echo $proc	
			path1=/data/memory/VmRSS_$proc.txt
			path2=/data/memory/VSZ_$proc.txt
			path3=/data/memory/mem_cpu.txt
			if [ ! $path1 ];then
				touch "$path"
			fi
			#监控总内存变化
			total_mem=$(free|grep Mem: |awk '{print $2,$3,$4,$5,$6,$7}')
			#监控cpu
			cpu=$(top -n 1 |grep CPU: | awk '{print $2}')
			
			echo $i $total_mem $cpu >> $path3

			s=$(top -n 1|grep $proc |awk  '{print $8}' |awk 'NR==1')
			if [ "$s" = "$proc" -o "$s" = "$App" ]
			then
				#监控进程的物理内存
				a=$(top -n 1 |grep $proc | awk '{print $1}' |awk 'NR==1')
				b=$(cat  /proc/$a/status |grep VmRSS | awk '{print $2}')
				#监控进程的虚拟内存
				c=$( top -n 1 |grep $proc |awk 'NR==1')
				
				if [ ! $a ]
				then
					echo "Unable to find" $proc >> $logpath

				else
					echo $proc " PID: "$a" ; VmRSS : "$b >> $logpath				
					echo $i $proc $a ":"$b >>  $path1
					echo $i $c >> $path2
				
				fi
			else
				echo $proc" is no exit !!!!!!" >> $logpath
			fi

		done
	i=$(($i+1))
	sleep 60
}
done








