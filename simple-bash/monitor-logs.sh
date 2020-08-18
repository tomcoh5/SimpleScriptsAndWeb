#!/bin/bash
logs=`cat /var/log/messages | grep 'New session'`
all=`echo $logs | xargs -n11 | sed '1d'`
while IFS= read -r line
do
  
  user=`echo $line | awk '{print $11}'`
  user="${user::-1}"
  date=`echo $line | awk '{print $1, $2, $3}'`
  echo $user has been logged in $date
done <<< "$all"
