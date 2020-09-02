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

class Connection():
   def __init__(self,of_dev,controller):
        self.DEBUG = False

        self.session = requests.Session()

        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


        # endereco da API
        self.API = 'http://{node}:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:{of}/table/0/flow/{{id}}'
        self.API = self.API.format(node=controller,of=of_dev)

        self.auth = HTTPBasicAuth('admin','admin')        # usuario de autenticacao
        self.url = self.API + self.REQUEST              # URL completa para requisição

   def doRequest(self,flow):
      url = self.API.format(id=flow['flow'][0]['id'])
      result = self.session.post(url, json=flow, auth=self.auth, headers=self.headers)

      if (self.DEBUG):
          print("{url}".format(url=self.url))
          print("{json}".format(json=flow))
          print(result)

      return result.status_code



class Flows():
    def __init__(self,generator):
        self.flow = {"flow": [{
                "id": "5",
                "cookie": 38,
                "instructions": {
                    "instruction": [{
                            "order": 0,
                            "apply-actions": {
                                "action": [{
                                        "order": 0,
                                        "drop-action": { }
                                    }]
                            }
                        }]},
                "hard-timeout": 65000,
                "match": {
                    "ethernet-match": {
                        "ethernet-type": {
                            "type": 2048
                        },
                        "ethernet-source": {
                            "address" : "fake"
                        }},
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
        self.generator = generator


    def createFlow(self):
        f = flow.copy()

        mac = self.generator.increment()

        f['flow'][0]['match']['ethernet-match']['ethernet-source']['address'] = self.generator.format_mac(mac)
        f['flow'][0]['flow-name'] = "TestFlow-%s" % mac
        f['flow'][0]['cookie_mask'] += 1
        f['flow'][0]['cookie'] += 1
        f['flow'][0]['id'] = mac

        return f



class Executor(threading.Thread):
   def __init__(self,of_dev,controller,generator):
      threading.Thread.__init__(self)

      self.connection = Connection(of_dev,controller)
      self.flows = Flows(of_dev,generator)

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
    def __init__(self, n = 3,execution_time = 10):
        self.threads = []

        ini_ip = 125
        self.n = n
        self.execution_time = execution_time

        self.generators = []

        for i in range(n):
            # Gerador de MACs sequenciais
            self.generators.append(MacGenerator())

            # Dev openflow para envio das regras
            of_dev=str(i+1)

            # Controlador para envio de fluxos
            controller = "192.168.247.{0}".format(ini_ip + i)

            # tempo de execução em segundos
            execution_time = 10

            n_threads = 128

            print(of_dev)
            print(controller)



            for n in range(n_threads):
                t = Executor(of_dev,controller,self.generators[i])
                self.threads.append(t)


    def start(self):
        # inicia as threads de envio para todos os controladores
        for t in self.threads:
            t.start()


        print("iniciando threads de envio de fluxos")
        for i in range(len(self.threads)):
            self.threads[i].started = True


        t = datetime.now()
        while((datetime.now() - t).total_seconds() <= self.execution_time):
            #print("Executando à ",(datetime.now() - t).total_seconds())
            sleep(1)
        else:
            # execucao completa
            print("execucacao completa, parando threads")

            for t in self.threads:
                t.active = False

        for t in self.threads:
            t.join()


        n_flows = 0
        for g in self.generators:
            n_flows += g.mac_value

        print("Fluxos enviados: %s" % n_flows)
