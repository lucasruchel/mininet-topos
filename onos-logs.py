#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink
from mininet.topo import LinearTopo

from functools import partial


import os
import time
import sys

from flows import executor

from tcpdump import capture

def emptyNet(n_control=3):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = LinearTopo(k=1,n=2)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers = []


    for i in range(n_control):
        posfix = i+5
        ip_address = "172.17.0.%d" % posfix

        controllers.append(net.addController('c%s' % i, controller=RemoteController, ip=ip_address, port=6633))

#    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.210", port=6633))


#    f = Flows()


#    capture("captura-3-nodes-odl-magnesium-events","eno1",timeout=180)

    net.build()
    net.start()

#    time.sleep(5*n_control)

   #Define o master, aguarda estabilidade dos backups e envia fluxos por 60 segundos
#    executor(n_control)

    # Tempo maximo para alcancar sincronia    
#    time.sleep(15)


    CLI(net)
    net.stop()


#    os.system("killall tcpdump")

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet(int(sys.argv[1]))

