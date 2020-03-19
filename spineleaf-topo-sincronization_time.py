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

from mastership_failover import failover
from tcpdump import capture

from flows import Flows

controllers = []

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = SpineLeaf(leaves=3)
    f = Flows()

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.5", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.17.0.6", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.17.0.7", port=6633))

    capture("inicio-conexao-com-testes","docker0",timeout=30)

    net.build()
    net.start()

    
    f.test()


    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")



#    os.system("killall tcpdump")
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()
 
