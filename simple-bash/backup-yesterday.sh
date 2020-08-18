#!/bin/bash
current_date=$(date +"%m-%d-%y")
file_path="/home/yuofvi/gopower"
backup_dir="/root/backup"
echo "Got it this is your file path $file_path"
echo "Searching for files ..."
touch $file_path/$current_date-backup.txt
cd $file_path
echo "Saving all the files"
echo "Making backup file"
for file in `find $file_path -type f -mtime -7 -exec ls -l {} \; | awk '{print $9}'`;do
        echo "adding $file for zip"
        final_backup+="$file"
        final_backup+=" "
        echo "Overwriting backup.txt file if used today"
        echo "" > $file_path/$current_date-backup.txt
        echo $file >> $file_path/$current_date-backup.txt
done
zip $backup_dir/$current_date-backup.zip $final_backup
