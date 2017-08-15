mosquitto_pub -f runjob.txt -h "130.186.13.80" -t "org/cineca/cluster/galileo/test/jobs_runjob" -d

#echo -n $res

sleep 1

mosquitto_pub -f exc_begin.txt -h "130.186.13.80" -t "org/cineca/cluster/galileo/test/jobs_exc_begin" -d
mosquitto_pub -f exc_begin_2.txt -h "130.186.13.80" -t "org/cineca/cluster/galileo/test/jobs_exc_begin" -d

#sleep 1

#mosquitto_pub -f exc_end.txt -h "130.186.13.80" -t "org/cineca/cluster/galileo/test/jobs_exc_end" -d


