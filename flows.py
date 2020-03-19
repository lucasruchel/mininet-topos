import requests
  
from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir
import json

class Flows():
    def __init__(self):
        self.auth = HTTPBasicAuth('onos','rocks')
        self.API = 'http://%s:8181/onos/v1'

        CLUSTER_INFO = "/cluster"

        node = self.API % "172.17.0.5"
        cluster = requests.get(node+CLUSTER_INFO, auth=self.auth)


        logging.basicConfig(filename="tempo_sincronia.log", level=logging.DEBUG)

        self.nodes = []
        for h in cluster.json()['nodes']:
            self.nodes.append(h['ip'])


    def flows(self):
        FLOWS = "/flows"

        consistent = False
        n_flows = {}

        print("verificando consistencia...")
        t_start = time()
        while (not consistent):
            for h in self.nodes:
                r = requests.get((self.API + FLOWS) % h, auth=self.auth)
                n_flows[h] = r.json()


            f_base = n_flows[self.nodes[0]]

            print("*"*100)
            print(f_base)
            consistent = True
            for h in self.nodes[1:]:
                if f_base != n_flows[h]:
                    consistent = False

        # Tempo em que foi alcancado a consistencia da visao de fluxos entre os controladores
        t_end = time()	
        synchronized = "Consistente em: %s s" % (t_end - t_start)
        print(synchronized)
        logging.debug(synchronized)


    def add_flow(self,of_dev,flow):
        REQUEST = "/flows?appId=rest"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

        result = requests.post((self.API+REQUEST) % '172.17.0.5', json=flow, auth=self.auth, headers=headers)
        print(result.status_code)

    def test(self):
        base_mac = "00:00:11:00:00:%02x"

        flow = {
            "priority": 40000,
            "timeout": 0,
            "isPermanent": "true",
            "deviceId": "of:0000000000000003",
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
        
        flows = {"flows" : [] }


        for i in range(2,255):
            f = flow.copy()
            f['selector']['criteria'][0]['mac'] = base_mac % i
            bug = json.dumps(f)

            flows['flows'].append(json.loads(bug))

        
        self.add_flow("of:0000000000000003",flows)
        self.flows()

    


if __name__ == "__main__":
        
        f = Flows()
        f.test()




