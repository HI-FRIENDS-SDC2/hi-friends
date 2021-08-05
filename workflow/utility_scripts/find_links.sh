#!/usr/bin/env bash

pattern2=`conda env export  --from-history | sed -n '/dependencies/,/prefix/p' | sed '1d; $d' | cut -d' ' -f 4- | cut -d'=' -f 1 | sed 's/$/-/'| paste -sd '|'`
#echo $pattern2
conda list --explicit | sed 's/=//g' | grep -E $pattern2 > /var/tmp/temp

# show the result
cat /var/tmp/temp

# remove the temp file
rm /var/tmp/temp

