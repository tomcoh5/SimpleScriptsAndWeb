#!/bin/bash
echo "showing user last log"
for user in `lastlog -b 0 -t 100 | sed '1d' | awk '{print $1, $4, $5, $6, $7}' | cut -f1 -d"+"
`;do
	display+=${user}	
	display+=" "
done
echo $display | sed 's/Tue//' | xargs -n4
