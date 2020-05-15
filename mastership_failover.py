import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir

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

    


class MasterChange(Thread):
       
         
   def __init__(self,of_dev,node_id,n_control):
       Thread.__init__(self)
       self.of_dev = of_dev
       self.node_id = node_id
       self.controllers = n_control
    
       self.auth = HTTPBasicAuth('onos','rocks')	
       self.D_API = 'http://%s:8181/onos/v1' % node_id
    
       self.mastership_req = {
          "deviceId": "of:0000000000000002",
          "nodeId": node_id,
          "role": "MASTER",
       }

       print(self.D_API)
 

   def assing_role(self):
        self.mastership_req['deviceId'] = self.of_dev
        print(self.mastership_req)

        result = requests.put(self.D_API+"/mastership", json=self.mastership_req, auth=self.auth)
        if (result.status_code != 200):
            print("Erro de comunicacao")
            return
        
        result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
        while (result.json()['master'] != self.node_id):
            sleep(1)
            result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
            print('Aguardando device %s' % self.of_dev)


        while (len(result.json()['backups']) < (self.controllers - 1)):
            sleep(1)
            result = requests.get(self.D_API+('/mastership/%s/role' % self.of_dev), auth=self.auth)
            print('Aguardando estabilidade %s' % self.of_dev)

        print(str(result.json()))

   def run(self):
        self.assing_role()

	
	

