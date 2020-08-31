#!/usr/bin/python
# coding: utf-8

import requests
  
from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread
from datetime import datetime

import logging
from os import path, mkdir
import json

from mastership import getOwner



class MacGenerator():
    def __init__(self):
        self.mac_value = 0


    def format_mac(self,mac):
    	assert len(mac) == 12  # length should be now exactly 12 (eg. 008041aefd7e)	
	assert mac.isalnum()  # should only contain letters and numbers

	# convert mac in canonical form (eg. 00:80:41:ae:fd:7e)
	mac = ":".join(["%s" % (mac[i:i+2]) for i in range(0, 12, 2)])

	return mac



    def increment(self):
	self.mac_value += 1
	mac = "{:012X}".format(int("0", 16) + self.mac_value)

	return self.format_mac(mac)




class Flows():
    def __init__(self):
        self.auth = HTTPBasicAuth('admin','admin')


        # API para adicionar fluxos
        self.API = 'http://{node}:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{{id}}'

        self.master_index = int(getOwner())
        self.master = "172.28.1.%s" % self.master_index

        self.API = self.API.format(node=self.master)

        self.generator = MacGenerator()
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.flow = {
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
                        },
                        "ethernet-source": {
                            "address" : "fake"
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
            }]}

        

    def add_flow(self,of_dev,flow):


        url = self.API.format(id=flow['flow'][0]['id'])

        result = requests.put(url, json=flow, auth=self.auth, headers=self.headers)

#        print("Sending flow to: %s" % url)
#        print("Flow {name}: {status}".format(name=flow['flow'][0]['flow-name'],status=result.status_code))

    def test(self):
        t = datetime.now()
        while((datetime.now() - t).total_seconds() < 180):
            f = self.flow.copy()

            f['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = self.generator.increment()
            f['flow'][0]['flow-name'] = "TestFlow-%s" % self.generator.mac_value
            f['flow'][0]['id'] = self.generator.mac_value
            bug = json.dumps(f)

            self.add_flow("of:0000000000000001",json.loads(bug))


        print("Fluxos enviados: %s" % self.generator.mac_value)


    def singleFlow(self):
            f = self.flow.copy()

            f['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = self.generator.increment()
            f['flow'][0]['flow-name'] = "TestFlow-%s" % self.generator.mac_value
            f['flow'][0]['id'] = self.generator.mac_value
            bug = json.dumps(f)

            self.add_flow("of:0000000000000001",json.loads(bug))


    # Informa o tamanho do cluster, para encontrar um nó ativo
    def getTableFlow(self,size):
        next_index = ((self.master_index+1)%size)+1

        new_master_index = getOwner(next_index)
        new_master = "172.28.1.%s" % new_master_index

        print("MASTER: {master}".format(master=new_master))

        D_API="http://{node}:8181".format(node=new_master)
        FLOW_TABLE_REQUEST="/restconf/operational/opendaylight-inventory:nodes/node/openflow:1/table/0/"

        result = requests.get(D_API+FLOW_TABLE_REQUEST,auth=self.auth,headers=self.headers)
        
        print("######### Flow table of Openflow:1 #############")
        print(result.json())

# Escolhe método de execução
def executor(single=False):
     
     f = Flows()

     if (single):
         f.singleFlow()
     else:
         f.test()

     return f.master_index

if __name__ == "__main__":
     executor()



