#!/bin/bash

for size in $(seq 3 7); do
	echo "Size $size"
	FILES=$(ls -tr ONOS_SIZE-$size-exec-*.mininet-registry.log)
	echo $FILES | wc
	
	cat $FILES | grep "Fluxos enviados:" | cut -f2 -d:
done
