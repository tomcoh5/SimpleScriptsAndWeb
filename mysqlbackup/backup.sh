#!/bin/bash
BACKUP_DIR="define your backup dir here"
DATE=$(date +%Y-%m-%d)
FILE="$BACKUPDIR/$DATE.SQL.gz"
USER="root"

unalias rm     2> /dev/null
rm ${FILE}     2> /dev/null
rm ${FILE}.gz  2> /dev/null

mysqldump -u $USER -p  --opt --all-databases > $FILE

gzip $FILE

echo "${FILE}.gz was created for today...:"
echo "now checking for files to delete..."

currentdate=$(date "+%Y-%m-%d")
for f in *.SQL.gz; do
	echo $f file
	extract=${f:0:10}
	echo $extract this is the date of the file
        year=${extract:0:4}
	echo $year this is the year of the file
        month=${extract:5:2}
	echo $month this is the month of the file
        day=${extract:8:2}
	echo $day this is the day of the file
        newdate="${year}"
        newdate+="-${month}"
        newdate+="-${day}"
        timestamp=$(date -d $newdate '+%Y-%m-%d')
        start_ts=$(date -d "$newdate" '+%s')
        end_ts=$(date -d "$currentdate" '+%s')
        day=$(( ( end_ts - start_ts )/(6060*24) ))
        if [ $day -lt 14 ];then
                echo "this file can stay $f "
        else
                echo "delete this file $f"
        fi

done
