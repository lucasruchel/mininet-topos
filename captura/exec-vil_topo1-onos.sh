$(timeout 50 sudo tcpdump -s 0  -w vilchez-topo1-onos.pcap -i s3-eth3)&

sleep 15

echo "Parando interface"
sudo ifconfig s2-eth2 down

sleep 15

echo "Acordando Interface"
sudo ifconfig s2-eth2 up
