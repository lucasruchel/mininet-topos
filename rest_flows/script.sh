#!/bin/bash

cluster_size=13

repeats=3

for i in $(seq 1 $repeats); do
	echo "############################"
	echo "Controlador: Onos"
	echo "Tamanho do cluster: $cluster_size"
	echo "Execucao: $i"
	echo "############################"

	sudo ~/testes/linear.py $cluster_size #| tee onos-$cluster_size-exec-$i.log
	
	# Aguarda alguns segundos para executar novamente
	sleep 10
done 
