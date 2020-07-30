#!/bin/bash
for word in ` cat /usr/local/apache2/logs/apache_access_log  | awk -F '[][]' '{print  $2}' `
do
        if  grep $word /usr/local/apache2/htdocs/log.html > /dev/null ;then

                echo "" >> hello.txt


        else

                echo "<p>" >> /usr/local/apache2/htdocs/log.html
                echo "$word" >> /usr/local/apache2/htdocs/log.html
                echo "</p>" >> /usr/local/apache2/htdocs/log.html
        fi
done
