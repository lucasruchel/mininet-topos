# encoding: utf-8

import requests
import threading

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread
from datetime import datetime



import logging
from os import path, mkdir
import json

from mac_utils import MacGenerator

import copy

class Connection():
   def __init__(self,of_dev,controller):
        self.DEBUG = False

        self.session = requests.Session()

        self.auth = HTTPBasicAuth('admin','admin')        # usuario de autenticacao
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


        # endereco da API
        self.API = 'http://{node}:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{of}/table/0/flow/{{id}}'
        self.MASTERSHIP_API = 'http://{node}:8181/restconf/operational/entity-owners:entity-owners'
 


        self.MASTERSHIP_API = self.MASTERSHIP_API.format(node=controller)

        controller = self.getMaster()

        self.API = self.API.format(node=controller,of=of_dev)





   def doRequest(self,flow):
      if self.DEBUG:
          print(flow)
     
      url = self.API.format(id=flow['flow'][0]['id'])

#      bug = json.dumps(flow)
#      flow = json.loads(bug)
      
      result = self.session.put(url, json=flow, auth=self.auth, headers=self.headers)

      if (self.DEBUG):
          print("URL: {url}".format(url=url))
          print("{json}".format(json=flow))
          print("HEADERS: {head}".format(head=self.headers))
          print("Mensagem: {result}".format(result=result.text))
          print(result)

      return result.status_code

   def getMaster(self):
        if self.DEBUG:
            print("Consultado API para definir o master")
            print("URL: {url}".format(url=self.MASTERSHIP_API))

        response = self.session.get(self.MASTERSHIP_API, auth=self.auth)

        if response.status_code == requests.codes.ok:
            r_obj = response.json()
            for entity in r_obj['entity-owners']['entity-type'][1]['entity']:
                if str(entity['id']).__contains__("openflow:1"):
                    return ("192.168.247." + entity['owner'][-3:])
                    

class Flows():
    def __init__(self,generator):
        self.flow = {   
#            "id": "5",
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
        
            
        self.generator = generator


    def createFlows(self):
        flows = {'flow' : []}



    
        mac = self.generator.increment()
           
        f = copy.deepcopy(self.flow)
        f['match']['ethernet-match']['ethernet-source']['address'] = self.generator.format_mac(mac)
        f['flow-name'] = "TestFlow-%s" % mac
        f['cookie_mask'] += 1
        f['cookie'] += 1
        f['id'] = mac

        flows['flow'].append(f)

        return flows



class Executor(threading.Thread):
   def __init__(self,of_dev,controller,generator):
      threading.Thread.__init__(self)

      self.active = True # Variavel de parada da thread
      self.started = False


   def run(self):
      while(self.active):
         # Aguarda inicio de todas as threads
         if(not self.started):
            sleep(0.01)
            continue

         # Cria flow e faz requisição ao controlador
         result = self.connection.doRequest(self.flows.createFlow())

         if (not(result == 200 or result == 201)):
             break


class Tester():
    """
        n - número de controladores
        execution_time - tempo de execução dos testes
    """
    def __init__(self):

        
        of_dev = "1"

        generator = MacGenerator()

        controller = "192.168.247.125"

        self.connection = Connection(of_dev,controller)
        self.flows = Flows(generator)



    def start(self,n):    

        print("Iniciando o envio de {flows} flows ".format(flows=n))
        for i in range(n):
            result = self.connection.doRequest(self.flows.createFlows())

        print("Execução completa")

#        t = datetime.now()
#        while((datetime.now() - t).total_seconds() <= self.execution_time):
            #print("Executando à ",(datetime.now() - t).total_seconds())
 #           sleep(1)

    def getMaster(self):
        return self.connection.getMaster()

if __name__ == "__main__":
    t = Tester()

    t.start(2)
