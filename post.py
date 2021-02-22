#!/usr/bin/env python3

import requests
import json
from datetime import datetime
from time import sleep
import sys


URL = 'http://ce13945d70eb.ngrok.io/api/PKAJCGSZ9XP3B366WANF/eSkW0UnRRLxYCdyRP72XZtF2fqlQYTMaZ4M1PsYj/endpoint'

timenow = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
ticker = sys.argv[1]
action = sys.argv[2]
contracts = int(sys.argv[3])
price = 200

data = {"side":f"{action}","ticker":f"{ticker}","size":f"{contracts}","price":f"{price}","sent":f"{timenow}"}


response = requests.post(URL,json=data)
print(response)
print(str(response.content))
