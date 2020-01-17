#!/bin/bash -x

export PATH=/usr/local/bin:/usr/bin:/sbin:/bin

home=$(cd $(dirname $0);pwd)
cd $home

ts=`date '+%Y-%m-%d %H:%M:%S'`
file="server.py"
logfile=$home/logs/tornado.log
for port in 51202;do
	if [ $# -eq 1 ]; then
		ps -ef | grep "$home/$file" |grep $port| grep -v "grep" | awk '{print $2}' | while read pid; do kill -9 $pid; done
		sleep 1
	fi

	cnt=$(ps -ef | grep  "$home/$file" |grep $port | grep -v "grep"| wc -l)
	if [ $cnt -eq 0 ];then
		echo $ts "server restart!" >> $logfile
		/usr/bin/python3 $home/$file --port=$port >> $logfile 2>&1 &
	fi
done
