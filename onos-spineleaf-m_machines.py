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
from flows import Flows

from mastership import changeTime
from tcpdump import capture

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = SpineLeaf(leaves=3)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="192.168.247.212", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="192.168.247.213", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="192.168.247.214", port=6633))

#    controllers.append(net.addController('c1', controller=RemoteController, ip="192.168.247.210", port=6633))


#    f = Flows()

#    capture("captura-3-nodes-odl-magnesium-events","eno1",timeout=180)

    net.build()
    net.start()

#    h1 = net.getNodeByName("h1")
#    h3 = net.getNodeByName("h3")

#    time.sleep(15)

#    devs = failover()
#    f.test()

#   time.sleep(5)

 #   for i in range(5,8):
 #       os.system("ssh onos@172.17.0.{0} -p 8101 -o StrictHostKeyChecking=no events -m > log_mastership_{0}.ini".format(str(i)))

 #   os.system("docker kill onos-1")
#    changeTime(devs)

#    h1.cmdPrint("ping -c 20 %s" % h3.IP()) 


 #   time.sleep(5)

 #   for i in range(5,8):
 #       os.system("ssh onos@172.17.0.{0} -p 8101 -o StrictHostKeyChecking=no events -m > log_mastership_{0}.end".format(str(i)))


    

    
#    time.sleep(25)



    CLI(net)
    net.stop()


#    os.system("killall tcpdump")

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

