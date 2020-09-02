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

import onosrest as Rest

def topology(n=3):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )

    topo = LinearTopo(k=3, n=1)

    f = Flows()

    net = Mininet(controller=RemoteController, switch=switch, topo=topo, build=False, autoSetMacs=True)

    for i in range(n):
        controllers.append(net.addController('c{0}'.format(i+1), controller=RemoteController, ip="192.168.247.{0}".format(125+i), port=6633))


    net.build()
    net.start()

    time.sleep(10)

    tester = Rest.Tester(n=n, execution_time=300)
    tester.start()

    time.sleep(10)

    # Desnecessario visto que sera automatico
#    CLI(net)
    net.stop()

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        topology(n=int(sys.argv[1]))
    else:
        topology()

