#!/bin/bash

DIR_INI=$(pwd)

for onos_size in $(seq 3 7); do

for execution in $(seq 1 20); do

	echo "###########################################"
	echo "Teste: Quantidade de fluxos pela API REST"
	echo "Execucao: $execution"
	echo "Tamanho do cluster: $onos_size"
	echo "###########################################"

	cd ~/onos-docker/

	./createCluster $onos_size

	cd $DIR_INI

	sleep 15

	# Captura trafego
#	sudo tcpdump  -w /mnt/onos_size-$onos_size-exec-$execution-mininet.pcap -i docker0 &


	# Inicia topologia com scripts de geração de tráfego
	sudo ~/testes/onos-linear-m_machines.py $onos_size > ONOS_SIZE-$onos_size-exec-$execution.mininet-registry.log 2>&1

	# Finaliza captura matando processo do tcpdump
#	sudo killall tcpdump

	for i in $(seq 1 $onos_size); do 
		docker logs onos-$i > ONOS_SIZE-$onos_size-exec-$execution.onos-$i.log
	done

	docker container kill $(docker ps -q); docker container rm $(docker ps -a -q)

done

done
