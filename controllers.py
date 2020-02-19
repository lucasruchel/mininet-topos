#!/usr/bin/python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController, OVSKernelSwitch
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI

setLogLevel( 'info' )

c0 = RemoteController('c0',ip="172.17.0.5", port=6633)
c1 = RemoteController('c1',ip="172.17.0.6", port=6633)
c2 = RemoteController('c2',ip="172.17.0.7", port=6633)


class MultiControllerSwitch(OVSSwitch):

    def start(self, controllers):
        return OVSSwitch.start(self,[{'c0': c0}])



topo = TreeTopo( depth=2, fanout=2 )
net = Mininet( controller=RemoteController, switch=MultiControllerSwitch, topo=topo )


net.start()
CLI( net )
net.stop()
