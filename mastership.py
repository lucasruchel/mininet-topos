#!/usr/bin/python
# -*- coding: utf-8

import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir

def trigger(index):
    auth = HTTPBasicAuth('admin','admin')

    D_API = 'http://172.28.1.%s:8181/restconf/operational/entity-owners:entity-owners' % index

    
    return requests.get(D_API, auth=auth)

# Passa opcionalmente o index do controlador
def getOwner(next_controller=3):
    index = None
    print("Aguardando conexão do Switch")
    # Repetir com um determinado atraso ate que seja encontrado a entidade para o switch
    while (index == None):
        response = trigger(next_controller)

        if (response.status_code == requests.codes.ok):
            r_obj = response.json()
        else:
            print("Aguardando inicio da API...")
            sleep(1)
            continue




        for entity in r_obj['entity-owners']['entity-type'][1]['entity']:
            if str(entity['id']).__contains__("openflow:1"):
                index = entity['owner'][-1]
                break
    
    sleep(1)


    return index





if __name__ == "__main__":
    print(getOwner())
