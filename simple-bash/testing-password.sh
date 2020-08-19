#!/bin/bash
echo "lets test your password"
sleep 1
echo " write it down"
read passwd
echo " this is your password $passwd"
limit=`echo -n $passwd | wc -c`
if [ "$limit" -lt 8 ];then
	echo "Error you password is not long enough"
	exit 1
else
	echo "your password length is okay, lets continue"
fi
re_number=[0-9]+$
sleep 1
if ! [[ $passwd  =~ $re_number ]] ; then
   echo "Error: no number has been found" >&2; exit 1
else
	echo "you have number in your passowrd, lets continue"
fi
sleep 1
checking_rm=`echo "$passwd" | sed 's/[^a-zA-Z0-9]//g'`
limit_checking=`echo -n $checking_rm | wc -c`


if [ $limit_checking -eq $limit ];then
	echo "Error:no non-alphabetic characters in your password"
	exit 1
else
	echo " you have non-alphabetic characters in your password"
fi
sleep 2
echo " the test have been comepleted "
