#!/bin/bash

for i in $(seq 10); do

## Recria o cluster
~/onos-docker/createCluster

## Inicia topologia e testes
sudo ./spineleaf-topo.py

## Limpa containers
docker container kill $(docker ps -q) && docker container rm $(docker ps -a -q)

done
