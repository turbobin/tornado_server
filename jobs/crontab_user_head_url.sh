#!/usr/bin/env bash

export PATH=/usr/local/bin:/usr/bin:/sbin:/bin

home=$(cd $(dirname $0);pwd)
cd $home

ts=`date +%Y%m%d_%H`
for ((i=0;i<2;i++));do
	file="loop_head_url_queue${i}.py"
	if [ $# -eq 1 ]; then
		ps -ef | grep "$home/$file" | grep -v "grep" | awk '{print $2}' | while read pid; do kill -9 $pid; done
		sleep 1
	fi

	cnt=$(ps -ef | grep  "$home/$file" | grep -v "grep"| wc -l)
	if [ $cnt -eq 0 ];then
		cp loop_head_url_queue.py $file
		/usr/bin/python3 $home/$file >> ./logs/${file}_${ts}.log 2>&1 &
	fi
done
