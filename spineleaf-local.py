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
from mastership import changeTime
from tcpdump import capture

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = SpineLeaf(leaves=3)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="192.168.247.210", port=6633))



#    capture("captura-3-nodes-odl","eno1",timeout=60)

    net.build()
    net.start()

    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")


#    devs = failover()

#    os.system("docker kill onos-1")
#    changeTime(devs)

#    h1.cmdPrint("ping -c 20 %s" % h3.IP()) 


 #  os.system("killall tcpdump")

    CLI(net)
    net.stop()



if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

