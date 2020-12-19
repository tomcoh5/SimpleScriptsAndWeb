#!/bin/bash

echo ""
echo "This script finds all the first level folders in the current folder,"
echo "and force overwrites them to a corresponding target folder, with the matching first letter folder"
echo "** it MUST be run in a Plugins folder **"
echo ""
echo "i.e. will move PlaylistRider.bundle to P/PlaylistRider.bundle"
echo ""
echo "Use to simplify the Plugins distributions to sub-folders"
echo ""



pwd | grep -q "Plugins$"

if [ "$?" -ne "0" ]
then
  exit 1
fi

total_miss=0
target_root=""
output=/tmp/output.txt
allow=0

while getopts t:o:a: flag
do
    case "${flag}" in
        t) target_root=${OPTARG};;
        o) output=${OPTARG};;
        a) allow=${OPTARG};;
    esac
done


count=0

pwd | grep -q 'Mac' && $target_root grep -q 'Mac' || count+=1

pwd | grep -q 'Win' && $target_root grep -q 'Win' || count+=1

if [[ $count -eq 2 ]];then
        echo "wrong path"
        exit 1
fi




#

if [[ -z "$target_root" ]]
then
  echo ""
  echo "error: missing argument TARGET_ROOT"
  echo "
usage: $0 -t TARGET_ROOT [-o OUTPUT_FILENAME] [-a NUM_NEW_ALLOWED]

        TARGET_ROOT - target plugins root folder (i.e. /commits/V12/Mac/Release/Plugins)
    OUTPUT_FILENAME - file to store copy commands (default: /tmp/output.txt)
    NUM_NEW_ALLOWED - proceed if no more than NUM_NEW_ALLOWED are missing on target (default: 0)
  "
  exit 1
fi

date
echo "
OUTPUT_FILENAME=$output
TARGET_ROOT=$target_root
NUM_NEW_ALLOWED=$allow
"

