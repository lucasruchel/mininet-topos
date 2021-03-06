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
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="172.18.0.6", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.18.0.3", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.18.0.5", port=6633))



#    capture("captura-3-nodes-odl-magnesium","eno1",timeout=60)

    net.build()
    net.start()

    h1 = net.getNodeByName("h1")
    h3 = net.getNodeByName("h3")


 #   devs = failover()
    
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
#    os.system("killall tcpdump")


    CLI(net)
    net.stop()



if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

