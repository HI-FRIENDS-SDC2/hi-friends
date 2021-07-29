now=`date +"%Y%m%d_%H%M%S"`
/mnt/scratch/sdc2/jmoldon/dstat/dstat -Tnlfvs -C total --output "dstat_${now}.csv" >> /dev/null &
P1=$!
echo $P1
#sleep 10 &
#time python run.py --check
time python run.py
P2=$!
echo $P2
wait $P2
kill $P1
