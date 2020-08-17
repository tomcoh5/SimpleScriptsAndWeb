#!/bin/bash
current_date=$(date "+%Y-%m-%d-%H:%M") >> /dev/null
echo current date $current_date
for f in *.SQL.gz; do
    extract=${f:0:16}
    echo extract $extract
    year=${extract:0:4}
    month=${extract:5:2}
    day=${extract:8:2}
    newdate="${year}"
    newdate+="-${month}"
    newdate+="-${day}"
    timestamp=$(date -d $newdate '+%Y-%m-%d')
    start_ts=$(date -d "$newdate" '+%s')
    end_ts=$(date -d "$currentdate" '+%s')
    day=$(( ( end_ts - start_ts )/(6060*24) ))

    #minutes and hour  extraction
    hourAndminute=${extract:11}
    date_only=${extract:0:10}
    timestamp_file=`date -d "$date_only $hourAndminute" +"%s"`
    timestamp_current=$(date +%s)
    diff=$(( $timestamp_current - $timestamp_file ))

    #function to display hour and minutes diff 
    convertsecs() {
 	((h=${1}/3600))
 	((m=(${1}%3600)/60))
 	((s=${1}%60))
 	printf "%02d:%02d:%02d\n" $h $m $s
	}    



    if [ $day -lt 1 ];then
            echo "backup has been made before $(convertsecs $diff) "
            return 1
            exit 0
    else
            echo "no backup has been made"
    fi

done
return 0

