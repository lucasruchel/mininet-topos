import requests
  
from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread
from datetime import datetime

import logging
from os import path, mkdir
import json

from mastership_failover import failover

class MacGenerator():
    def __init__(self):
        self.mac_value = 0


    def format_mac(self,mac):

	# convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
        mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])

        return mac



    def increment(self):
        self.mac_value += 1
        mac = "{:012X}".format(int("0", 16) + self.mac_value)

        return self.format_mac(mac)


	



class Flows():
    def __init__(self):
        self.auth = HTTPBasicAuth('onos','rocks')
        self.API = 'http://%s:8181/onos/v1'

        CLUSTER_INFO = "/cluster"

        node = self.API % "172.17.0.5"

        self.generator = MacGenerator()

        self.flow = {
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
 



    def add_flow(self,of_dev,flow):
        REQUEST = "/flows/%s?appId=rest" % of_dev
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        result = requests.post((self.API+REQUEST) % '172.17.0.5', json=flow, auth=self.auth, headers=headers)

    def test(self):

        t = datetime.now()
        while((datetime.now() - t).total_seconds() < 180):
            f = self.flow.copy()
            f['selector']['criteria'][0]['mac'] = self.generator.increment()
            bug = json.dumps(f)

            self.add_flow("of:0000000000000001",json.loads(bug))

        print("Fluxos enviados: %s" % self.generator.mac_value)

    def single(self):
        f = self.flow.copy()
        f['selector']['criteria'][0]['mac'] = self.generator.increment()
        bug = json.dumps(f)

        self.add_flow("of:0000000000000001",json.loads(bug))

        print("Fluxos enviados: %s" % self.generator.mac_value)


    


def executor(n_control=3,unique=False):
     failover(n_control)
     
     f = Flows()

     if (unique):
         f.single()
     else:
         f.test()

if __name__ == "__main__":
     executor(n_control=3)



