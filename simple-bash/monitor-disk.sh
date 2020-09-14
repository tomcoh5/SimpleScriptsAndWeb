#!/bin/bash

today_date=$(date "+%Y_%m_%d")
mounted_disk_devices=$(lsblk | awk '{print $7}')
disk_usage_percent=$1

for mounted_disk_device in ${mounted_disk_devices};
do
    if [[ ${mounted_disk_device} = '' ]]; then
        continue;
    fi;

    if [[ ${mounted_disk_device} = 'MOUNTPOINT' ]]; then
        continue;
    fi;

    if [[ ${mounted_disk_device} = '[SWAP]' ]]; then
        continue;
    fi;

    disk_usage=$(df -lh ${mounted_disk_device} | tail -n 1 | awk '{print $5}' | sed -e 's/%//g')
    if [[ ${disk_usage} -gt ${disk_usage_percent} ]]; then
        message="Disk mount point: ${mounted_disk_device} should be considered."
        echo ${message}
        echo ${message} >> "disk_usage_${today_date}.txt"
    fi;
done;
