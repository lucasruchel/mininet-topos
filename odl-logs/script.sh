#!/bin/bash


for n in $(seq 1 20); do

cd ~/testes/odl-logs/

~/odl-docker/opendaylight/createCluster.sh 7


sudo ~/testes/odl-linear-m_machines.py 7 > odl_size-7-exec-$n-odl-registry.log


for i in $(seq 1 7); do
	docker logs odl-$i > odl_size-7-exec-$n-odl-$i.log
done

cd ~/odl-docker/opendaylight/ && docker-compose --project-directory ~/odl-docker/opendaylight/ down -t 1


done
