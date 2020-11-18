#!/bin/bash
echo "command[check_php-fpm]=/usr/local/nagios/libexec/php-fpm.sh" >> /etc/nrpe.cfg
chown nagios:nagios /usr/local/nagios/libexec/php-fpm.sh
service xinetd restart
