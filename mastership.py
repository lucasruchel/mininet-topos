#!/usr/bin/python3

import requests

from requests.auth import HTTPBasicAuth

from time import sleep, time
from threading import Thread

import logging
from os import path, mkdir

def trigger():
    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://172.17.0.5:8181/onos/v1'

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']




    mastership_req = {
             "deviceId": "of:0000000000000002",
             "nodeId": "172.17.0.5",
             "role": "MASTER",
        }
    headers = {'content-type': 'application/json'}




    for dev in devices:
        mastership_req['deviceId'] = dev['id']

        result = requests.put(D_API+"/mastership", json=mastership_req, auth=auth)
        print(result.status_code)

        
        sleep(5)
        print(D_API+('/mastership/%s/master' % dev['id']))       
        result = requests.get(D_API+('/mastership/%s/master' % dev['id']), auth=auth)
        
        print("Master de %s : %s" % (dev['id'],result.json()['nodeId']))

class MasterCheck(Thread):
    
    def __init__(self, node,log_path):
        Thread.__init__(self)
        self.node = node
        self.log_path = log_path

    def run(self):


        auth = HTTPBasicAuth('onos','rocks')
        
        D_API = 'http://172.17.0.6:8181/onos/v1'

        result = requests.get(D_API+("/mastership/%s/master" % self.node), auth=auth)

        curr_master = "172.17.0.5"
        tstart = time()

        nro_requests = 0
        while (result.json()['nodeId'] == curr_master):
            result = requests.get(D_API+("/mastership/%s/master" % self.node), auth=auth)
            nro_requests += 1
            sleep(0.0001)

        tend = time()


        logging.basicConfig(filename=self.log_path, level=logging.INFO)

        logging.info("%s:Tempo para novo master is %s -- requests: %d" % (self.node,str(tend - tstart),nro_requests))
    
        
def checkStart():
    log_dir = "capturas/"
    log_file = "mastership_changeTime_log_%s.txt"

    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://172.17.0.5:8181/onos/v1'

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']

    log_number = 1
    log_path = log_dir+log_file % log_number
    while (path.exists(log_path)):
        log_path = log_dir + log_file % log_number
        log_number += 1



    for dev in devices:
        thread = MasterCheck(dev['id'],log_path)
        thread.start()

