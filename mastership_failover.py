# encoding: utf-8

import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir
from datetime import datetime

def failover(n_control=3):
    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://172.17.0.5:8181/onos/v1'

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']

    threads = []
    devs = []
    print("failover...")
    print(devices)
    for dev in devices:
        t = MasterChange(dev['id'],'172.17.0.5',n_control)
        devs.append(dev['id'])

        t.start()
        print("iniciando Thread para %s" % dev['id'])
        threads.append(t)

    for t in threads:
        t.join()

    return devs

def get_master(host="172.17.0.6"):
    auth = HTTPBasicAuth('onos','rocks')   
    
    D_API = 'http://%s:8181/onos/v1' % host
    MASTERSHIP = '/mastership/%s/role'
    DEVICES = '/devices'

    result = requests.get(D_API+DEVICES,auth=auth)
    devices = result.json()['devices']

    # Testes possuem um único dispositivo, pegando ID dele
    dev = devices[0]['id']

    # Pega papeis dos controladores conectaods
    result = requests.get(D_API+(MASTERSHIP % dev),auth=auth)
    mastership = result.json()

    return mastership['master']

        

    


def new_master(host="172.17.0.6"):
    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://%s:8181/onos/v1' % host

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']

    threads = []
    devs = []
#    print("failover...")
#    print(devices)

    # ENDPOINT do ONOS para identificar o papel dos controladores
    MASTERSHIP_ROLE_REQUEST="/mastership/%s/role"

    # primeiro dispositivo, como a topologia que estamos testando é com um único dispositivo
    s1 = devices[0]

    result = requests.get(D_API+(MASTERSHIP_ROLE_REQUEST % s1['id']),auth=auth)

    if (result.status_code == 200):
        nMaster =  result.json()["master"]
    else:
        return

    FLOW_TABLE_REQUEST = "/flows/{deviceId}".format(deviceId=s1['id'])
    D_API = 'http://%s:8181/onos/v1' % nMaster
   
    result = requests.get(D_API+FLOW_TABLE_REQUEST,auth=auth)

    if (result.status_code == 200):
        print(result.json())

    return None



class MasterChange(Thread):
       
         
   def __init__(self,of_dev,node_id,n_control):
       Thread.__init__(self)
       self.of_dev = of_dev
       self.node_id = node_id
       self.controllers = n_control
    
       self.auth = HTTPBasicAuth('onos','rocks')	
       self.D_API = 'http://%s:8181/onos/v1' % node_id
    
       self.mastership_req = {
          "deviceId": "of:0000000000000001",
          "nodeId": node_id,
          "role": "MASTER",
       }

       print(self.D_API)
 


   def assing_role(self):
        self.mastership_req['deviceId'] = self.of_dev
#        print(self.mastership_req)

        result = requests.put(self.D_API+"/mastership", json=self.mastership_req, auth=self.auth)
        if (result.status_code != 200):
            print("Erro de comunicacao")
            return
        
        result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
        while (result.json()['master'] != self.node_id):
            requests.put(self.D_API+"/mastership", json=self.mastership_req, auth=self.auth)
            sleep(1)
            result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
            print('Aguardando device %s' % self.of_dev)


        ts = datetime.now()
        while ((len(result.json()['backups']) < (self.controllers - 1)) and ((datetime.now() - ts).total_seconds() < 60)):
            sleep(1)
            result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
            print('Aguardando estabilidade %s' % self.of_dev)

        print("Tempo para estabilidade: %s" % (datetime.now() - ts).total_seconds())
        print(str(result.json()))

   def run(self):
        self.assing_role()

	
	

