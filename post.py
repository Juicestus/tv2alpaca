#!/usr/bin/env python3

import requests
import json
from datetime import datetime
from time import sleep
import sys

URL = 'http://localhost:5000/api/PK0PK2NE98R9PMBHN0IJ/7k2PG3wWOXbqA03M1OkEwH2MsQhIy0eLL43LKz1T/endpoint'

timenow = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
ticker = 'AAPL'
action = sys.argv[1]
contracts = int(sys.argv[2])
price = 200

data = {"side":f"{action}","ticker":f"{ticker}","size":f"{contracts}","price":f"{price}","sent":f"{timenow}"}


response = requests.post(URL,json=data)
print(response)
print(str(response.content))
