$(timeout 50 sudo tcpdump -s 0  -w vilchez-topo3-onos.pcap -i s3-eth5)&

sleep 15

echo "Parando interface"
sudo ifconfig s4-eth3 down

sleep 15

echo "Acordando Interface"
sudo ifconfig s4-eth3 up
