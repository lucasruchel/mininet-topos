import requests
  
from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir
import json

from mastership import getOwner

class Flows():
    def __init__(self):
        self.auth = HTTPBasicAuth('admin','admin')


        # API para adicionar fluxos
        self.API = 'http://%s:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/5'


        self.API = self.API % getOwner()



    def add_flow(self,of_dev,flow):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        result = requests.put(self.API, json=flow, auth=self.auth, headers=headers)

        print("Sending flow to: %s" % self.API)
        print(result)

    def test(self):

       
	flow = {
    "flow": [
        {   
            "id": "5",
            "cookie": 38,
            "instructions": {
                "instruction": [
                    {   
                        "order": 0,
                        "apply-actions": {
                            "action": [
                                {   
                                    "order": 0,
                                    "drop-action": { }
                                }
                            ]
                        }
                    }
                ]
            },
            "hard-timeout": 65000,
            "match": {
                "ethernet-match": {
                    "ethernet-type": {
                        "type": 2048
                    }
                },
                "ipv4-destination": "10.0.0.38/32"
            },
            "flow-name": "TestFlow-1",
            "strict": False,
            "cookie_mask": 4294967295,
            "priority": 2,
            "table_id": 0,
            "idle-timeout": 65000,
            "installHw": False
        }

    ]
}



        
        self.add_flow("of:0000000000000001",flow)
#        self.flows()

    


def executor():
     
     f = Flows()
     f.test()

if __name__ == "__main__":
     executor()



