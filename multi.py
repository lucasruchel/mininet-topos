#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def emptyNet():
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    controllers = []
 
    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.5", port=6633))
    controllers.append(net.addController('c2', controller=RemoteController, ip="172.17.0.6", port=6633))
    controllers.append(net.addController('c3', controller=RemoteController, ip="172.17.0.7", port=6633))

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')


    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')


    net.addLink(s1,h1)
    net.addLink(s1,h2)
    net.addLink(s1,s2)

    net.addLink(s2,h3)
    net.addLink(s2,h4)
    net.addLink(s2,s3)

    net.addLink(s3,h5)
    net.addLink(s3,h6)
    net.addLink(s3,s1)
    
    
    
    net.build()
    
    for c in range(len(controllers)):
        c.start()


    s1.start(controllers)
    s2.start(controllers)
    s3.start(controllers)

    net.start()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet()

