#!/bin/bash

DIR_INI=$(pwd)

for onos_size in $(seq 3 7); do

for execution in $(seq 1 5); do

	echo "###########################################"
	echo "Teste: Packet-In do switch"
	echo "Execucao: $execution"
	echo "Tamanho do cluster: $onos_size"
	echo "###########################################"

	cd ~/onos-docker/

	./createCluster $onos_size

	cd $DIR_INI

	sleep 15

	# Captura trafego
	sudo tcpdump  -w /mnt/onos_size-$onos_size-exec-$execution-packetIn-mininet.pcap -i docker0 &


	# Inicia topologia com scripts de geração de tráfego
	sudo ~/testes/onos-linear-packet_in.py $onos_size > /mnt/onos_size-$onos_size-exec-$execution-packetIn.mininet-registry.log 2>&1

	# Finaliza captura matando processo do tcpdump
	sudo killall tcpdump

#	for i in $(seq 1 $onos_size); do 
#		docker logs onos-$i > /mnt/ONOS_SIZE-$onos_size-exec-$execution-packetIn.onos-$i.log
#	done

	docker container kill $(docker ps -q); docker container rm $(docker ps -a -q)

done

done
