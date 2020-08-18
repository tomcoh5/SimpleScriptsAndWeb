#!/bin/bash
file_path="/home/yuofvi/gopower"
backup_dir="/root/backup"
echo "Got it this is your file path $file_path"
echo "Searching for files ..."
cd $file_path
pwd
if [[ -f "save.txt" ]]; then
	rm -f save.txt
fi
touch save.txt
echo "Saving all the files"
echo "Making backup file"
for file in `find $file_path -type f -mtime -7 -exec ls -l {} \; | awk '{print $9}'`;do
	echo making back up for $file
	tar -cvf $backupdir/$file.tar
	echo $file >> save.txt
done

	
