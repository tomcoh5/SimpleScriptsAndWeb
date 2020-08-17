#!/bin/bash
read $pid 
if ps -p $PID > /dev/null
then
	echo "$PID is running"
	echo "do you want to remove it ?"
	read tellme
	if [ $tellme == "yes" ];then
		kill -9 $PID
	else
		echo "okay goodbye"
	fi
else
	echo "$PID i cant seems to find it"
fi
