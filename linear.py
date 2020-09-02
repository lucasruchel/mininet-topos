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

from onosrest import Tester

def topology():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )

    topo = LinearTopo(k=3, n=1)

    f = Flows()

    net = Mininet(controller=RemoteController, switch=switch, topo=topo, build=False, autoSetMacs=True)

    controllers.append(net.addController('c1', controller=RemoteController, ip="192.168.247.125", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="192.168.247.126", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="192.168.247.127", port=6633))


    net.build()
    net.start()

    time.sleep(10)

    tester = Tester()
    tester.start()

    time.sleep(10)
    # Desnecessario visto que será automático
    #CLI(net)
    net.stop()

if __name__ == "__main__":
    topology()
