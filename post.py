#!/usr/bin/env python3

# Written by Justus Languell, jus@gtsbr.org, 2021

import requests
import json
from datetime import datetime
from time import sleep
import sys


URL = 'http://tv2alpaca.com/api/PKJXYKZJX9KXCFM4OMY9/WR3ovOzjnRL8z3vh11Ytszo2AMBTiOuL9J026Hpa/endpoint'


timenow = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
ticker = sys.argv[1]
action = sys.argv[2]
contracts = int(sys.argv[3])
price = 200

data = {"side":f"{action}","ticker":f"{ticker}","size":f"{contracts}","price":f"{price}","sent":f"{timenow}"}


response = requests.post(URL,json=data)
print(response)
print(str(response.content))
