#!/bin/sh
testmax=10
i=0
while [ $i -lt $testmax ]
do
    ubus call device.wiegrand write '{"length":8,"data":"12345678"}'
    sleep 1
        i=$(($i+1))
done
