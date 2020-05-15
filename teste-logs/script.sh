#!/bin/bash

DIR_INI=$(pwd)

for onos_size in $(seq 4 7); do

for execution in $(seq 1 $1); do

	cd ~/onos-docker/

	./createCluster $onos_size

	cd $DIR_INI

	sleep 15

	sudo ~/testes/onos-linear-m_machines.py $onos_size


	for i in $(seq 1 $onos_size); do 
		docker logs onos-$i > ONOS_SIZE-$onos_size-exec-$execution.onos-$i.log
	done

	docker container kill $(docker ps -q); docker container rm $(docker ps -a -q)

done

done
