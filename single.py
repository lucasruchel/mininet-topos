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
import sys

from mastership_failover import failover
from tcpdump import capture

from flows import Flows

controllers = []

import onosrest as OnosRest
import odlrest as OdlRest

def topology(n=1):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )

    topo = LinearTopo(k=n, n=1)

    f = Flows()

    net = Mininet(controller=RemoteController, switch=switch, topo=topo, build=False, autoSetMacs=True)

    for i in range(n):
        controllers.append(net.addController('c{0}'.format(i+1), controller=RemoteController, ip="172.17.0.2", port=6633))


    net.build()
    net.start()


    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")

    n = 1
    if (len(sys.argv) == 2):
        n = int(sys.argv[1])

    topology(n=n)

