#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink
from mininet.topo import LinearTopo

from functools import partial

from topos import SpineLeaf

import os
import time

from mastership_failover import failover
from tcpdump import capture

from flows import Flows

controllers = []

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )

    topo = LinearTopo(k=2, n=2)

    f = Flows()

    net = Mininet(controller=RemoteController, switch=switch, topo=topo, build=False, autoSetMacs=True)

    controllers.append(net.addController('c1', controller=RemoteController, ip="192.168.247.125", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="192.168.247.126", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="192.168.247.127", port=6633))


    net.build()
    net.start()

    
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()
 
