#!/bin/bash

cluster_size=3

repeats=5

for i in $(seq 0 $repeats); do
	echo "############################"
	echo "Tamanho do cluster: $cluster_size"
	echo "Execucao: $i"
	echo "############################"

	sudo ~/testes/linear.py $cluster_size #| tee onos-$cluster_size-exec-$i.log
	
	# Aguarda alguns segundos para executar novamente
	sleep 10
done
