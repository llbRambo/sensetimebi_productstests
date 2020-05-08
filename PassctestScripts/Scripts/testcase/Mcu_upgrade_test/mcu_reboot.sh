#!/bin/sh
line=$(tail -n -1 /data/record.txt)
times=$(($line+1))
echo $times >> /data/record.txt
