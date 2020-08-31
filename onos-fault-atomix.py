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

from flows import executor
from mastership_failover import get_master

from tcpdump import capture

def host_send(node):
    node.cmdPrint("/home/ti/testes/scapy-test.py","3000")



def emptyNet(n_control=3):
    switch = partial( OVSSwitch, protocols='OpenFlow13' )
    link = partial(TCLink, bw=100)
    topo = LinearTopo(k=1,n=2)

    net = Mininet(controller=RemoteController, switch=switch, link=link, topo=topo, build=False, autoSetMacs=True)

    controllers = []


    for i in range(n_control):
        posfix = i+n_control+2
        ip_address = "172.17.0.%d" % posfix

        controllers.append(net.addController('c%s' % i, controller=RemoteController, ip=ip_address, port=6633))

#    controllers.append(net.addController('c1', controller=RemoteController, ip="172.17.0.210", port=6633))


#    f = Flows()



#    capture("captura-3-nodes-odl-magnesium-events","eno1",timeout=180)

    net.build()
    net.start()


    time.sleep(10)

    # Com isso temos o IP  do MASTER, mas é necessário saber a instância do docker,  sabemos que é onos-1==172.17.0.5, primeiro octeto para definir instância
    ip_master = get_master(ip_address)
    master = int(ip_master.split('.')[-1]) - n_control - 1



    h1 = net.getNodeByName("h1s1")
    t = Thread(target=host_send, args=[h1,])
    t.start()
   
   #Define o master, aguarda estabilidade dos backups e envia fluxos por 60 segundos, segundo parâmetro fluxo único
#    executor(n_control,True)

    # Aguarda até que tenha instalado alguns fluxos
    time.sleep(10)

    # Mata o container docker do onos e atomix
    print("Falhando controlador atomix-1")
#    os.system("docker kill --signal=9 onos-%s" % master)
    os.system("docker kill --signal=9 atomix-1")
 
    # Sincroniza com a thread de envio de fluxos
    t.join()

    # Aguarda mais um tempo para conclusão de envio dos fluxos
#    time.sleep(10)

#    print("######### OVS-OFCTL dump before crash ###########")
    print(os.popen("ovs-ofctl dump-flows -O openflow13 s1").read())

#    print("######### OVS-VSCTL lista controladores before crash #########")
#    print(os.popen("ovs-vsctl list controller").read())

    # Bloqueia conexões com iptables
#    os.system("iptables -A INPUT -s 172.17.0.5 -j DROP")
#    os.system("iptables -A OUTPUT -d 172.17.0.5 -j DROP")

   



    
#    print("######### OVS-OFCTL dump after crash ###########")
#    print(os.popen("ovs-ofctl dump-flows -O openflow13 s1").read())

#    print("######### OVS-VSCTL lista controladores after crash #########")
#    print(os.popen("ovs-vsctl list controller").read())

#    print("######### OF CONTROLLER dump do novo controlador MASTER através da API #######")
#    new_master()


#    CLI(net)
    net.stop()

    # Desfaz bloqueio do iptables
#    os.system("iptables -D OUTPUT 1")
#    os.system("iptables -D INPUT 1")

    

if __name__ == "__main__":
    setLogLevel("info")
    emptyNet(int(sys.argv[1]))

