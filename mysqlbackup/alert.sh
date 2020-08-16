#!/bin/bash
current_date=$(date "+%Y-%m-%d-%H:%M") >> /dev/null
for f in *.SQL.gz; do
	extract=${f:0:16}
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

    #time and hour extraction

    current_hour=${currentdate:11:16}
    conv_current_hour=$(echo $current_hour | awk -F: '{ print ($1 * 3600) + ($2 * 60) }')
    hour_minutes=$(echo $exe | awk -F: '{ print ($1 * 3600) + ($2 * 60) }')
    diff=$(( $conv_current_hour - $hour_minutes ))
    #function to display hour and minutes diff 
    diff=${diff:1}
    function displaytime {
  	local T=$1
  	local D=$((T/60/60/24))
  	local H=$((T/60/60%24))
  	local M=$((T/60%60))
  	local S=$((T%60))
  	(( $H > 0 )) && printf '%d hours ' $H
  	(( $M > 0 )) && printf '%d minutes ' $M
  	(( $D > 0 || $H > 0 || $M > 0 )) && printf 'and '
  	printf '%d seconds\n' $S
     }




    if [ $day -lt 1 ];then
            echo "backup has been made before $(displaytime $diff)"
            return 1
            exit 0
    else
            echo "no backup has been made"
    fi

done
return 0

