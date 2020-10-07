#!/bin/bash

event_command="ssh onos@localhost -p 8101 events -f"

if [ ! -d dados ]; then
        mkdir dados
fi


## For para definição do tamanho do cluster
for i in $(seq 6 13); do

# For para os fluxos
for f in 128 256 512 1024 2048 4096; do

if [ $i -eq 6 ] && [ ! $f -eq 4096 ]; then
	continue
fi

# For para repetições
for r in $(seq 1 3); do

echo "##########################################"
echo "execucação: $r"
echo "size: $i"
echo "fluxos $f"
echo "##########################################"



# For para instanciacao dos hosts no cluster
for j in $(seq 1 $i); do
	ssh ti@192.168.247.$((124+$j)) nohup ~/onos/startup.sh > ~/startup.log 2>&1 &

	# Se a instancia for maior do que 3 aguarda um periodo para que as 3 iniciais iniciem e as posteriores
	if [ $j -gt 3 ]; then
	   sleep 300
	fi
done

sleep 300

# Cria topologia
sudo /home/ti/testes/linear.py $i $f > dados/mininet-cluster_size-$i-exec-$r-flows-$f.log

# For para captura dos dados
for j in $(seq 1 $i); do
	ip=192.168.247.$((124+$j)) 
	ssh ti@$ip $event_command >> dados/onos_size-$i-exec-$r-flows-$f-$ip.events.log
done


# For parar os processos
for j in $(seq 1 $i); do
	ip=192.168.247.$((124+$j)) 

	ssh ti@$ip pkill java

	sleep 30
	ssh ti@$ip pkill -9 java

	# Se a instancia for menor ou igual a 3, remove dados do atomix
	if [ $j -le 3 ]; then
		ssh ti@$ip rm -rf atomix/data/
	fi

done

# Limpa mininet caso tiver dado algum problema
sudo mn -c

done
done
done
















