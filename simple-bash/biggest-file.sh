#!/bin/bash
echo "Hello, this is a script for checking biggest files in a spesific directory"
sleep 1
echo "Write down the path to the directory"
read d_path
echo "processing ..."
sleep 1
echo "Creating log file for deleting files in /root named delete.txt"
touch /root/delete.txt
echo "" > /root/delete.txt
echo "log file for deleting files" >> delete.txt
sleep 1
IFS=$'\n'
files=`du -ah $d_path | grep -v "/$" | sort -rh | head | sed '1d'`
for file in `echo $files | xargs -n2`;do
	echo "$file"
	echo " do you want to remove this file ?"
	read tellme
	if [ $tellme == "yes" ];then
		echo "Removing $file ..."
		echo $file >> /root/delete.txt
	else
		echo "ok i will continue"
	fi 
	sleep 2
done 
sleep 2
echo "that's it, goodbye, if you cant remeber the files that have been deleted. you should go to /root/delete.txt"
exit 1
