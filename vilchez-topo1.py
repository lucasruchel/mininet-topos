#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink

from functools import partial


import os

def emptyNet():
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=10)
    net = Mininet(controller=RemoteController, switch=switch, link=link)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.5", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.17.0.6", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.17.0.7", port=6633))

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')


    net.addLink(s4,h1)
    net.addLink(s4,s2)


    net.addLink(s2,s1)

    net.addLink(s1,s3)


    net.addLink(s3,s5)
    net.addLink(s3,s6)

    net.addLink(s5,h2)

    net.addLink(s6,h3)
    
    
    
    net.build()
    
#    for c in range(len(controllers)):
#        controllers[c].start()




    net.start()


    h3.cmd("netserver -4 -p 50500")

    CLI(net)
    net.stop()
    os.system("killall netserver  2>&1")

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

