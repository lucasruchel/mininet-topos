#!/bin/bash

for i in $(seq 10); do

## Recria o cluster
~/onos-docker/manyLocations

## Inicia topologia e testes
sudo ./spineleaf-topo-dsites.py

## Limpa containers
docker container kill $(docker ps -q) && docker container rm $(docker ps -a -q)

done
