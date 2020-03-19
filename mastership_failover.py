import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir

def failover():
    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://172.17.0.6:8181/onos/v1'

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']

    threads = []
    for dev in devices:
        t = MasterChange(dev['id'],'172.17.0.5')
        t.start()
        print("iniciando Thread para %s" % dev['id'])
        threads.append(t)

    for t in threads:
        t.join()


class MasterChange(Thread):
       
         
   def __init__(self,of_dev,node_id):
       Thread.__init__(self)
       self.of_dev = of_dev
       self.node_id = node_id
    
       self.auth = HTTPBasicAuth('onos','rocks')	
       self.D_API = 'http://172.17.0.6:8181/onos/v1'
    
       self.mastership_req = {
          "deviceId": "of:0000000000000002",
          "nodeId": "172.17.0.5",
          "role": "MASTER",
       }
 

   def assing_role(self):
        self.mastership_req['deviceId'] = self.of_dev
        result = requests.put(self.D_API+"/mastership", json=self.mastership_req, auth=self.auth)
        if (result.status_code != 200):
            print("Erro de comunicacao")
            return
        	
        result = requests.get(self.D_API+('/mastership/%s/master' % self.of_dev), auth=self.auth)
        while (result.json()['nodeId'] != self.node_id):
            sleep(1)
            result = requests.get(self.D_API+('/mastership/%s/master' % self.of_dev), auth=self.auth)
            print('Aguardando device %s' % self.of_dev)

   def run(self):
        self.assing_role()

	
	
	
