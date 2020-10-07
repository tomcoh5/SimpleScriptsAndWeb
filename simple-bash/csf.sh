#!/bin/bash
if [ -f "go.txt"];then
        echo "" > go.txt
else
        touch go.txt
fi
cat  /var/log/apache2/domlogs/* | awk '{print $1,$6}' | grep POST  >> go.txt
if [ -f "attack.txt" ];then
        echo "" > attack.txt
else
        touch attack.txt
fi
sort go.txt | uniq -cd | awk -v limit=100 '$1 > limit{print $2}' >> attack.txt
ips=`cat attack.txt`
cloudflare=`cat cloudflare.txt`
for ip in $ips;do
        if [ `curl -s ipinfo.io/$ip | grep country | cut -d":" -f2 | tr -d '",'` != "IL" ];then
                 csf -d $ip
        fi
done
for cloud in $cloudflare;do
         csf -a $cloud
done
