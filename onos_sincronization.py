# encoding: utf-8

import requests
import threading
import json

from requests.auth import HTTPBasicAuth

from time import sleep, time
from datetime import datetime

from mac_utils import MacGenerator

import copy

class Connection():
   def __init__(self,controller):
        self.DEBUG = False

        self.session = requests.Session()

        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.REQUEST = "/flows?appId=rest"

        self.auth = HTTPBasicAuth('onos','rocks')        # usuario de autenticacao
        self.API = 'http://%s:8181/onos/v1' % controller # endereco da API

        self.url = self.API + self.REQUEST              # URL completa para requisição


   def doRequest(self,flow, more=False):
      result = self.session.post(self.url, json=flow, auth=self.auth, headers=self.headers)

      if (self.DEBUG):
          print("{url}".format(url=self.url))
          print("{json}".format(json=flow))
          print(result)

      if (result.status_code == 200 and more):
          return result.json()

      return result.status_code

"""
    Informação dos dispositivos
"""
class Switches():
    def __init__(self,controller):
        self.DEBUG = False

        self.session = requests.Session()

        self.headers = {'Accept': 'application/json'}
        self.REQUEST = "/devices"

        self.auth = HTTPBasicAuth('onos','rocks')        # usuario de autenticacao
        self.API = 'http://%s:8181/onos/v1' % controller  # endereco da API
        self.url = self.API + self.REQUEST              # URL completa para requisição

    def getDevices(self):
        devices = self.session.get(self.url,auth=self.auth, headers=self.headers )

        if (devices.status_code == 200):
            devices = devices.json()['devices']
            available = []

            # Verifica somente os dispositivos disponiveis
            for d in devices:
                if (d['available'] == True):
                    available.append(d)

            if (len(available) > 0):
                return available

        return None

class Mastership():
    def __init__(self,controller):
        self.DEBUG = False

        self.session = requests.Session()
        self.headers = {'Accept': 'application/json'}
        self.auth = HTTPBasicAuth('onos','rocks')        # usuario de autenticacao
        self.API = 'http://%s:8181/onos/v1' % controller  # endereco da API


        # Endpoints da API
        self.BALANCE = '/mastership'
        self.MASTER = '/mastership/{deviceId}/master'
        self.CLUSTER = '/cluster'


    def balance(self):
        url = self.API + self.BALANCE
        response = self.session.get(url,auth=self.auth,headers=self.headers)

        return response.status_code

    def getMaster(self,of_dev):
        endpoint_master = self.MASTER.format(deviceId=of_dev)
        url = self.API + endpoint_master

        response = self.session.get(url,auth=self.auth,headers=self.headers)

        if (response.status_code == 200):
            node = response.json()['nodeId']
            return node

        return None

    def getClusterNodes(self):
        url = self.API + self.CLUSTER

        response = self.session.get(url,auth=self.auth, headers=self.headers)

        if (response.status_code == 200):
            nodes = response.json()['nodes']
            return nodes

        return None

class Flows():
   def __init__(self,generator):
      self.generator = generator

      self.bFlow = {
            "priority": 40000,
            "timeout": 0,
            "isPermanent": "true",
            "deviceId": "of_dev",
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


   def createFlow(self,of_dev):
      f = copy.deepcopy(self.bFlow)
      f['deviceId'] = of_dev
      f['selector']['criteria'][0]['mac'] = self.generator.getMAC()

      return f




class Tester():
    """
        n - número de controladores
        execution_time - tempo de execução dos testes
    """
    def __init__(self,api):

        self.DEBUG = False


        self.api = api

        # Gerador de MACs sequenciais
        self.generator = MacGenerator()
        self.sw = Switches(controller=self.api)
        self.mastership = Mastership(controller=self.api)
        self.flows = Flows(self.generator)


    def start(self, n = 128):
        generated_flows = []

        switches = self.sw.getDevices()
        of_dev = None
        if (switches != None and len(switches) > 0):
            of_dev = switches[0]['id']

        if (of_dev == None):
            print("of_dev not found!")
            return

        for i in range(n):
            f = self.flows.createFlow(of_dev)
            generated_flows.append(f)

        self.master = self.mastership.getMaster(of_dev)

        if (self.master == None):
            print("ERRO: NÃO ENCONTRADO NENHUM MASTER!!!!!!!")
            return

        cluster_nodes = self.mastership.getClusterNodes()

        self.connection = Connection(controller=self.master)

        backups = []
        for b in cluster_nodes:
            if (b['ip'] != self.master and b['status'] == 'READY'):
                backups.append(b)

        if (self.DEBUG):
            print(backups)



        content = {'flows': generated_flows }

        print("MASTER CONTROLLER: ",self.master)

        # flow_IDs instalados
        api_flows = self.connection.doRequest(flow=content, more=True)

        print(api_flows)

        if (self.DEBUG):
            print(api_flows)
