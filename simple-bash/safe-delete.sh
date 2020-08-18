#!/bin/bash
echo "Hello welcome to safe delete"
cd $HOME
echo $PWD
sleep 1
if [ ! -d "$HOME/trash" ]; then
	echo " you already have trash folder, great :D"
else:
	echo "you dont have trash folder creating now..."
	mkdir trash
fi
sleep 1
ls -la
echo " is there any files you would like to send to trash ? "
read tellme
sleep 1
if [ $tellme == "yes" ];then
	echo "great, write down the files path"
	sleep 1
	read files
	echo "chaning names for the files"
	sleep 1
	for name in $files;do
		mv $name $name-before-delete
	done
	sleep 1
	echo $files 
	mv "files" "$HOME/trash"
	echo "Done"
else
	echo "ok lets continue"
fi
sleep 1
echo "now lets check if we have any files in the folder that are more than 48 hours"
sleep 1
find $HOME/trash -mtime -2 -ls
if [ $? -eq 0 ];then
	echo "i found files older than 48 hours"
	echo "removing files ..."
else
	echo "i didnt found files older than 48 hours"
fi
sleep 1
echo " i will exit , cya next time"
exit
