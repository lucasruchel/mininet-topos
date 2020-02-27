#!/usr/bin/python3

import requests

from requests.auth import HTTPBasicAuth

def trigger():
    auth = HTTPBasicAuth('onos','rocks')

    D_API = 'http://172.17.0.5:8181/onos/v1'

    result = requests.get(D_API+'/devices', auth=auth)

    devices = result.json()['devices']




    mastership_req = {
             "deviceId": "of:0000000000000002",
             "nodeId": "172.17.0.7",
             "role": "MASTER",
        }
    headers = {'content-type': 'application/json'}




    for dev in devices:
        mastership_req['deviceId'] = dev['id']

        result = requests.put(D_API+"/mastership", json=mastership_req, auth=auth)
        print(result.status_code)
