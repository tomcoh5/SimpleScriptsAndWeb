#!/bin/bash
lucky=7
for num in {1000..10000};do
	num_one=`echo $num | cut -c1`
	num_two=`echo $num | cut -c2`
	num_three=`echo $num | cut -c3`
	num_four=`echo $num | cut -c4`
	num_five=`echo $num | cut -c5`
	sum=$(( num_one + num_two + num_three + num_four + num_five ))
	if [ $sum -eq "7" ];then
		echo $num is a lucky number
		echo "" >> /dev/null
	fi
	num_one_b=`echo $sum | cut -c1`
	num_two_b=`echo $sum | cut -c2`
	sum_two=$(( num_one_b + num_two_b ))
	if [ $sum_two -eq "7" ];then
		echo $num is a lucky number
	fi
done
