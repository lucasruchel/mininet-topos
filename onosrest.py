# encoding: utf-8

import requests
import threading
import json

from requests.auth import HTTPBasicAuth

from time import sleep, time
from datetime import datetime

from mac_utils import MacGenerator


class Connection():
   def __init__(self,of_dev,controller):
        self.DEBUG = False

        self.session = requests.Session()

        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.REQUEST = "/flows/%s?appId=rest" % of_dev

        self.auth = HTTPBasicAuth('onos','rocks')        # usuario de autenticacao
        self.API = 'http://%s:8181/onos/v1' % controller # endereco da API

        CLUSTER_INFO = "/cluster"                        # ENDPOINT para informacoes do cluster


        self.url = self.API + self.REQUEST              # URL completa para requisição


   def doRequest(self,flow):
      result = self.session.post(self.url, json=flow, auth=self.auth, headers=self.headers)

      if (self.DEBUG):
          print("{url}".format(url=self.url))
          print("{json}".format(json=flow))
          print(result)

      return result.status_code


class Flows():
   def __init__(self,of_dev,generator):
      self.generator = generator

      self.bFlow = {
            "priority": 40000,
            "timeout": 0,
            "isPermanent": "true",
            "deviceId": of_dev,
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


   def createFlow(self):
      f = self.bFlow.copy()
      f['selector']['criteria'][0]['mac'] = self.generator.getMAC()

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

        self.generators = []

        for i in range(n):
            # Gerador de MACs sequenciais
            self.generators.append(MacGenerator())

            # Dev openflow para envio das regras
            of_dev="of:000000000000000{0}".format(i+1)

            # Controlador para envio de fluxos
            controller = "192.168.247.{0}".format(ini_ip + i)

            # tempo de execução em segundos
            execution_time = 10

            n_threads = 128

            print(of_dev)
            print(controller)



            for n in range(n_threads):
                t = Executor(of_dev,controller,generators[i])
                threads.append(t)


    def start(self):
        # inicia as threads de envio para todos os controladores
        for t in threads:
            t.start()

        for i in range(len(threads)):
            threads[i].started = True

        t = datetime.now()
        while((datetime.now() - t).total_seconds() <= execution_time):
            print("Executando à ",(datetime.now() - t).total_seconds())
            sleep(1)
        else:
            for t in threads:
                t.active = False

        for t in threads:
            t.join()


        n_flows = 0
        for g in generators:
            n_flows += g.mac_value

        print("Fluxos enviados: %s" % n_flows)
