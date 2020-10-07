#!/bin/bash
url=`cat /etc/domainusers | awk '{print $2}'`
for domain in $url;do
        if nc -zw1 $domain 443;then
                echo $domain >> ok.txt
        else
                echo $domain >> notok.txt
        fi
done
