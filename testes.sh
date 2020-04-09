#!/bin/bash

for i in $(seq 10); do

## Recria o cluster
$1

## Inicia topologia e testes
sudo ./spineleaf-topo-sincronization_time.py

## Limpa containers
docker  kill $(docker ps -q) && docker container rm $(docker ps -a -q)

mv capturas/tempo_sincronia.log capturas/tempo_sincronia.log.$i

done
