#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink

from functools import partial

from topos import SpineLeaf

import os
import time

from mastership import trigger, checkStart
from tcpdump import capture

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = SpineLeaf(leaves=3)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.5", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.17.0.6", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.17.0.7", port=6633))

    net.build()
    net.start()

    trigger()

    time.sleep(5)

    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")


    log_output = "iperf_log_"
    log_index = 1
    log_dir = "capturas/"
    log_path = log_dir+log_output+str(log_index)

    while os.path.exists(log_path):
        log_index += 1
        log_path = log_dir+log_output+str(log_index)

    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
        

#    h3.cmdPrint("iperf -s -p 3434 &")
    h3.cmdPrint("iperf --udp -s -p 3434 &")
#    h1.cmdPrint("iperf -c 10.0.0.3 -p 3434 -t 60 -b 100000000")
    h1.cmdPrint("iperf -c 10.0.0.3 --udp -p 3434 -t 50 -b 100000000 >> %s &" % (log_path))
    
    capture("falha-controlador-s3-eth2","s3-eth2",timeout=40)            
    capture("falha-controlador-s3-eth1","s3-eth1",timeout=40)            

    time.sleep(15)



    os.system("docker container stop onos-3")

    checkStart()

    time.sleep(15)
    
#    CLI(net)
    net.stop()
    os.system("killall iperf  2>&1")

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

