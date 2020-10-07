#!/bin/bash

curr_dir=$(pwd)


if [ ! -d dados ]; then
        mkdir dados
fi

if [ ! -d logs_odl ]; then
	mkdir logs_odl
fi


## For para definição do tamanho do cluster
for i in $(seq 4 13); do

# Troca o diretorio para execução do script
cd /home/ti/testes/ansible/

##### Gera arquivos de configuracao para o ODL
/home/ti/testes/ansible/generator_config.py -s $i
/home/ti/testes/ansible/generator_inventory.py -s $i

ansible-playbook -i inventory.json ansible_odl.yml --extra-vars "@conf.json"

cd $curr_dir

# For para os fluxos
for f in 128 256 512 1024 2048 4096; do

# For para repetições
for r in $(seq 1 5); do

echo "##########################################"
echo "execucação: $r"
echo "size: $i"
echo "fluxos $f"
echo "##########################################"

# For para instanciacao dos hosts no cluster
echo 'Iniciando processos!!'
for j in $(seq 1 $i); do
	echo "iniciando 192.168.247.$((124+$j))"  
	ssh ti@192.168.247.$((124+$j)) sudo systemctl start opendaylight
done




sleep 300

sudo tcpdump  -w /mnt/odl_size-$i-exec-$r-flows-$f-mininet.pcap -i eno1 &

# Cria topologia
sudo /home/ti/testes/linear.py $i $f > dados/mininet-cluster_size-$i-exec-$r-flows-$f.log



# For parar os processos
echo 'Parando processos!!'
for j in $(seq 1 $i); do
	ip=192.168.247.$((124+$j)) 

	ssh ti@$ip sudo systemctl stop opendaylight
	ssh ti@$ip sudo rm -rf ~/odl/opendaylight-0.12.0/data/
done

sudo killall tcpdump

# Limpa mininet caso tiver dado algum problema
sudo mn -c

done
done
done
















