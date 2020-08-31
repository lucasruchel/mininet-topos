import requests
import threading
  
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
        
	return mac




class Flows():
    def __init__(self,generator):
        self.auth = HTTPBasicAuth('admin','admin')


        # API para adicionar fluxos
        self.API = 'http://{node}:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/{{id}}'


        self.API = self.API.format(node=getOwner())

        self.generator = generator
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.session = requests.Session()

    def add_flow(self,of_dev,flow):


        url = self.API.format(id=flow['flow'][0]['id'])

        result = self.session.put(url, json=flow, auth=self.auth, headers=self.headers)

#        print("Sending flow to: %s" % url)
#        print(str(result))

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
        }

    ]
}

        t = datetime.now()
        while((datetime.now() - t).total_seconds() < 60):
            f = flow.copy()

            mac = self.generator.increment()

            f['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = self.generator.format_mac(mac)
            f['flow'][0]['flow-name'] = "TestFlow-%s" % mac
            f['flow'][0]['cookie_mask'] += 1
            f['flow'][0]['cookie'] += 1
            f['flow'][0]['id'] = mac
            bug = json.dumps(f)

            self.add_flow("of:0000000000000001",json.loads(bug))





       
        
        self.add_flow("of:0000000000000001",flow)
#        self.flows()

    


def executor(generator):
     
     f = Flows(generator=generator)
     f.test()

if __name__ == "__main__":
     generator = MacGenerator()

     threads = []
     for i in range(4):
         t = threading.Thread(target=executor,args=(generator,))
         threads.append(t)
         t.start()
    
    
     for x in threads:
            x.join()


     print("Fluxos enviados: %s" % generator.mac_value)     
