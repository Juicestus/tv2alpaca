#!/usr/bin/env python3

# Written by Justus Languell, jus@gtsbr.org, 2021
# Really shitty code but it does the job

import requests
import json
from datetime import datetime
from time import sleep
import sys

if __name__ == '__main__':

    if sys.argv[1] == 'order':
        domain = 'tv2alpaca.com' if sys.argv[2] == 'com' else 'localhost:' + sys.argv[2]
        keys = [l.replace('\n','') for l in open('alpacakeys')]

        URL = f'http://{domain}/api/{keys[0]}/{keys[1]}/endpoint'


        timenow = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
        ticker = sys.argv[3]
        action = sys.argv[4]
        contracts = int(sys.argv[5])
        price = None

        data = {"side":f"{action}","ticker":f"{ticker}","size":f"{contracts}","price":f"{price}","sent":f"{timenow}"}

        response = requests.post(URL,json=data)
        print(response)
        print(str(response.content))
        print(f'Req sent with keys: {keys}')
        print('To url: ' + URL)

    if sys.argv[1] == 'set':
        f = open('alpacakeys','w')
        f.write(sys.argv[2] + '\n' + sys.argv[3])
        f.close()

    if sys.argv[1] == 'help' or '-h' in sys.argv:
        print('''
    Set keys args: set <key1> <key2>
    Send to com args: order com <ticker> <side> <contracts>
    Send to loacl args: order <port> <ticker> <side> <contracts>
    ''')


