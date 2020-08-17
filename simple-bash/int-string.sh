#!/bin/bash
echo "pass an argument"
read $arugement
re='^[0-9]+$'
if ! [[ "$arguement" =~ "$re" ]] ; then
   echo "error: Not a number" >&2; 

else
	echo "the arugement is a number"
	exit 1
fi

if [ -z "$arugement" ]
then
      echo "\$arugement is empty"
else
      echo "\$the arugement is string"
fi
