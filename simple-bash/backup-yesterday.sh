#!/bin/ibash
echo "write down file path"
read $file_path
echo "how many days you want to look back?"
read $days
find $file_path -type f -mtime -$days -print
