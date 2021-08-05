#!/usr/bin/env bash

## grep the part before 'dependencies:'
#conda env export  --no-build | sed '/dependencies/q' > /var/tmp/temp

# prepare the pattern for packages installed explicitly ('conda=|python=|pytest=|scipy=|pandas=', for instance)
pattern=`conda env export  --from-history | sed -n '/dependencies/,/prefix/p' | sed '1d; $d' | cut -d' ' -f 4- | cut -d'=' -f 1 | sed 's/$/=/' | paste -sd '|'`
#echo $pattern

# filter the output with --no-build using the pattern prepared
conda env export  --no-build | grep -E $pattern >> /var/tmp/temp

## grep the part after 'prefix:'
#conda env export  --from-history | sed -ne '/prefix/,$p' >> /var/tmp/temp

# show the result
cat /var/tmp/temp

# remove the temp file
rm /var/tmp/temp

