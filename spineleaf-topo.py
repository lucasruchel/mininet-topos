#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink

from functools import partial

from topos import SpineLeaf

import os

from mastership import trigger

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = SpineLeaf(leaves=3)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.5", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.17.0.6", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.17.0.7", port=6633))

    net.build()
    net.start()

    trigger()

    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")

    h3.cmdPrint("iperf --udp -s -p 3434 &")
    h1.cmdPrint("iperf -c 10.0.0.3 --udp -p 3434 -t 30 -b 100000000")

    CLI(net)
    net.stop()
    os.system("killall iperf  2>&1")

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

