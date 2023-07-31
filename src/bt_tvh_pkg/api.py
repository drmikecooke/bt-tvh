# ideas from:

# https://github.com/Finn10111/tvh-auto-power/blob/master/tvh-auto-power.py

# https://github.com/dave-p/TVH-API-docs/wiki/

import requests
from requests.auth import HTTPDigestAuth
import time
from json import loads
from os import environ

statkeys=["input","ber","ec_bit","ec_block","tc_bit","tc_block","te","cc","unc"]

def getAPI(api):
    try:
        response=requests.get(__URL__+api,auth=HTTPDigestAuth(__USER__,__PWD__))
    except requests.ConnectionError:
        return {'help':0} # indicate not connected
    return loads(response.text,strict=False)

def setUSR(host):
    global __USER__,__PWD__,__URL__
    __URL__=f'http://{host}:9981/api/'
    if "TVH" in environ:
        __USER__,__PWD__=environ["TVH"].split(":")
    else:
        __USER__,__PWD__=input("user: "),input("pwd: ")
    
def subs():
    hd=getAPI("status/subscriptions")
    return [entry['title'] for entry in hd['entries']]
    
def inputs():
    sd=getAPI('status/inputs')['entries'][0]
    return {key:sd[key] for key in statkeys}

def nxt():
    gd=getAPI("dvr/entry/grid_upcoming")
    if gd['total']>40:
        print(f'Check all entries for {ip}\n')
    starts=[item['start_real'] for item in gd['entries']]
    stops=[item['stop_real'] for item in gd['entries']]
    if starts:
        return min(starts),min(stops)
    return None,None
