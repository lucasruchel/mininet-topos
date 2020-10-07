#!/usr/bin/python


from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink
from mininet.topo import LinearTopo

from functools import partial

from topos import SpineLeaf
from threading import Thread

import os
import time
import sys

from mastership_failover import failover
from tcpdump import capture

from odl_sincronization import Tester

controllers = []

def host_send(node):
    node.cmdPrint("/home/ti/testes/scapy-test.py","10000")



def topology(n=3,flows_number=128):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )

    topo = LinearTopo(k=1, n=n)


    net = Mininet(controller=RemoteController, switch=switch, topo=topo, build=False, autoSetMacs=True)

    for i in range(n):
        controllers.append(net.addController('c{0}'.format(i+1), controller=RemoteController, ip="192.168.247.{0}".format(125+i), port=6633))


    net.build()
    net.start()

    time.sleep(15)

    # No que enviara trafego
    h1s1 = net.getNodeByName("h1s1")

#    tester = Tester(api="192.168.247.125")
    tester = Tester()

    # master do switch atual
    master = tester.getMaster()


    # Envio de mensagens 1000 pcks_in/s
    t = Thread(target=host_send, args=[h1s1,])

    # comando para parar servico remoto
    print(os.popen("sudo -u ti ssh ti@{master} sudo systemctl stop opendaylight".format(master=master)))

    time.sleep(60)

    # Desnecessario visto que sera automatico
#    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    if (len(sys.argv) == 3):
        n = int(sys.argv[1])
        flow = int(sys.argv[2])
        topology(n = n, flows_number = flow)

    else:
        topology()

