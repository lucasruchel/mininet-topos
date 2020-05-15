#!/usr/bin/python3

import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir

def trigger():
    auth = HTTPBasicAuth('admin','admin')

    D_API = 'http://172.28.1.3:8181/restconf/operational/entity-owners:entity-owners'

    
    return requests.get(D_API, auth=auth)

def getOwner():
    response = trigger()
    r_obj = response.json()

    index = r_obj['entity-owners']['entity-type'][0]['entity'][0]['owner'][-1]

    return "172.28.1.%s" % index





if __name__ == "__main__":
    print(getOwner())
