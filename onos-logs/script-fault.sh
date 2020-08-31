#!/bin/bash

DIR_INI=$(pwd)

for onos_size in $(seq 3 3); do

for execution in $(seq 1 1); do

	echo "###########################################"
	echo "Tamanho do cluster: $onos_size"
	echo "Execucao: $execution"
	echo "###########################################"

	cd ~/onos-docker/

	./createCluster $onos_size

	cd $DIR_INI

	sleep 15

	# Captura trafego
	sudo tcpdump  -w /mnt/onos_size-$onos_size-exec-$execution-fault-mininet.pcap -i docker0 &


	# Inicia topologia com scripts de geração de tráfego
	sudo ~/testes/onos-linear-fault-rest.py $onos_size > ONOS_SIZE-$onos_size-exec-$execution-fault.mininet-registry.log 2>&1

	# Finaliza captura matando processo do tcpdump
	sudo killall tcpdump

	for i in $(seq 1 $onos_size); do 
		docker logs onos-$i > ONOS_SIZE-$onos_size-exec-$execution-fault.onos-$i.log
	done

	docker container kill $(docker ps -q); docker container rm $(docker ps -a -q)

done

done
