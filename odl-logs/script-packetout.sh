#!/bin/bash

PATH_ODL="/home/ti/odl-docker/opendaylight"

# Tamanho do cluster
for size in $(seq 3 7); do

cd "$PATH_ODL"

# Configura arquivos em modo cluster
./clusterConfig.sh $size

# Refaz imagem
docker build . -t teste


	# Número de repetições a serem feitas
	for n in $(seq 1 5); do

		echo "####################"
		echo "Execucao: $n"
		echo "Tamanho do cluster: $size"
		echo "####################"

		

		# Configurações iniciais do cluster
		$PATH_ODL/createCluster.sh $size
		
		# Aguarda até que inicialização do ambiente seja completada
		echo "Aguardando um tempo para que controladores iniciem..."
		sleep 150


		# Configura aplicação do controlador para negar pacotes
		for i in $(seq 1 $size); do 
			docker exec -it odl-$i bin/client dropallpacketsrpc on
		done		


		# inicia captura
		sudo tcpdump  -w /mnt/odl_size-$size-exec-$n-packetout.pcap -i br-$(docker network ls --filter="name=odl_net" -q) &



#		cd ~/testes/odl-logs/
		sudo ~/testes/odl-packetout.py $size > /mnt/odl_size-$size-exec-$n-packetout.log 2>&1
		
		# finaliza captura
		sudo killall tcpdump

		# Loop para gerar o log das instâncias
#		for i in $(seq 1 $size); do
#			docker logs odl-$i > odl_size-$size-exec-$n-odl-$i.log
#		done

#		mv *.log /mnt/

		# Para cluster de controladores
		cd $PATH_ODL && docker-compose down -t 1

	# Fim do loop de repetições
	done

# Fim do loop do tamanho do cluster
done
