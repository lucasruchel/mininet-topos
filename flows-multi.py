import requests
  
from requests.auth import HTTPBasicAuth

from time import sleep, time
import threading
from datetime import datetime

import logging
from os import path, mkdir
import json

from mastership_failover import failover

class MacGenerator():
    def __init__(self):
        self.mac_value = 1
        self.lock = threading.Lock()


    def format_mac(self,mac):
      # convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
      mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])


        
      return mac



    def increment(self):
        self.lock.acquire()

        self.mac_value += 1
        mac = "{:012X}".format(int("0", 16) + self.mac_value)
        
        self.lock.release()
        
        return self.format_mac(mac)


	



class Flows():
    def __init__(self,generator,of_dev):
        self.session = requests.Session()


        self.auth = HTTPBasicAuth('onos','rocks')
        self.API = 'http://%s:8181/onos/v1'

        CLUSTER_INFO = "/cluster"

        self.node = self.API % "172.17.0.5"

        self.generator = generator
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.REQUEST = "/flows/%s?appId=rest" % of_dev

        self.url = self.node + self.REQUEST


    def add_flow(self,flow):
        result = self.session.post(self.url, json=flow, auth=self.auth, headers=self.headers)

    def test(self):

        flow = {
            "priority": 40000,
            "timeout": 0,
            "isPermanent": "true",
            "deviceId": "of:0000000000000001",
            "treatment": {
                "instructions": [
                {
                    "type": "OUTPUT",
                    "port": "2"
                }
            ]},
            "selector": {
                "criteria": [
                    {
                        "type": "ETH_SRC",
                        "mac": "00:00:11:00:00:%02x"
                        },
                    {
                        "type": "ETH_DST",
                        "mac": "00:00:11:00:00:01"
                    },
                    {
                        "type": "IN_PORT",
                        "port": "1"
                    },
                ]
            }
        }
        

        t = datetime.now()
        while((datetime.now() - t).total_seconds() < 60):
            f = flow.copy()
            f['selector']['criteria'][0]['mac'] = self.generator.increment()
            bug = json.dumps(f)

            self.add_flow(json.loads(bug))


    


def executor(generator):
     f = Flows(generator=generator,of_dev="of:0000000000000001")
     f.test()

if __name__ == "__main__":
     generator = MacGenerator()
     failover(3)

     threads = []
     for i in range(12):
         t = threading.Thread(target=executor,args=(generator,))
         threads.append(t)
         t.start()
    
    
     for x in threads:
            x.join()


     print("Fluxos enviados: %s" % generator.mac_value)     




