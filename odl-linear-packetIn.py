#!/usr/bin/python
# coding: utf-8

from mininet.net import Mininet
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCIntf, TCLink
from mininet.topo import LinearTopo

from functools import partial
from threading import Thread

import os
import time
import sys

from odl_flows import Flows
from mastership import getOwner
#from tcpdump import capture

def host_send(node):
    node.cmdPrint("/home/ti/testes/scapy-test.py","300")



def emptyNet(n_control=3):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = LinearTopo(k=1,n=2)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)


    controllers = []


    for i in range(n_control):
        posfix = i+1
        ip_address = "172.28.1.%d" % posfix

        controllers.append(net.addController('c%s' % i, controller=RemoteController, ip=ip_address, port=6633))


    net.build()
    net.start()

    # Aguarda até que haja estabilidade dos controladores após conexão dos switches
    time.sleep(5*n_control)


    # Cria objeto de comunicação com API REST
#    flows = Flows()


    # Envia fluxo para a API
 #   flows.singleFlow()

    master = getOwner()

    h1 = net.getNodeByName("h1s1")
    t = Thread(target=host_send, args=[h1,])
    t.start()
 
    

    # Tempo necessário para instalação de regras no ONOS
    time.sleep(10)

#    print("######### OVS-OFCTL dump before crash ###########")
#    print(os.popen("ovs-ofctl dump-flows -O openflow13 s1").read())

#    print("######### OVS-VSCTL lista controladores before crash #########")
#    print(os.popen("ovs-vsctl list controller").read())

    # Bloqueia conexões com iptables
#    os.system("iptables -A INPUT -s 172.17.0.5 -j DROP")
#    os.system("iptables -A OUTPUT -d 172.17.0.5 -j DROP")

    # Mata o container docker
    print(os.popen("docker kill --signal=9 odl-%s" % master).read())
    
    t.join()

    # Tempo maximo para alcancar sincronia    
    time.sleep(10)

    
#    print("######### OVS-OFCTL dump after crash ###########")
#    print(os.popen("ovs-ofctl dump-flows -O openflow13 s1").read())

    print("######### OVS-VSCTL lista controladores after crash #########")
    print(os.popen("ovs-vsctl list controller").read())

#    flows.getTableFlow(n_control)

#    time.sleep(1)

#    CLI(net)
    net.stop()


#    os.system("killall tcpdump")

if __name__ == "__main__":
    setLogLevel("info")

    if (len(sys.argv) == 2):
        emptyNet(int(sys.argv[1]))
    else:
        emptyNet()

