#!/bin/bash

PATH_ODL="/home/ti/odl-docker/opendaylight"
MAX_SIZE=7
MAX_EXEC=5


# Tamanho do cluster
for size in $(seq 3 $MAX_SIZE); do

cd "$PATH_ODL"

# Configura arquivos em modo cluster
./clusterConfig.sh $size

# Refaz imagem
docker build . -t teste


	# Número de repetições a serem feitas
	for n in $(seq 1 $MAX_EXEC); do

		echo "####################"
		echo "Execucao: $n"
		echo "Tamanho do cluster: $size"
		echo "####################"


		# Configurações iniciais do cluster
		$PATH_ODL/createCluster.sh $size

		# inicia captura de tráfego
		sudo tcpdump  -w /mnt/odl_size-$size-exec-$n-packetIn.pcap -i br-$(docker network ls --filter="name=odl_net" -q) &

		cd ~/testes/odl-logs/
		sudo ~/testes/odl-linear-packetIn.py $size > odl_size-$size-exec-$n-packetIn.log 2>&1
		
		# finaliza captura
		sudo killall tcpdump

		# Loop para gerar o log das instâncias
		for i in $(seq 1 $size); do
			docker logs odl-$i > odl_size-$size-exec-$n-odl-$i-packetIn.log
		done

		mv *.log /mnt/
		
		cd $PATH_ODL && docker-compose down -t 1

	# Fim do loop de repetições
	done

# Fim do loop do tamanho do cluster
done
