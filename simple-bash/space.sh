#!/bin/bash
echo "write file path"
read file_path
echo "how many empty lines you want"
read num
x=$num
if [ $num -eq 1 ];then
	 cat $file_path | sed 'G' > $file_path
elif [ $num -gt 1 ];then
	while [ $x -gt 1 ];do
	        cat $file_path | sed 'G' > "$filepath"
		x=$(($x-1))
	done
fi
