#!/usr/bin/env python3

# A less shitty version of the
# tv2alpaca test client
# Written by Justus Languell jus@gtsbr.org, 2021
# See poster.cpp for my C++ version I wrote for practice

import requests
import sys
from datetime import datetime
import os

KEYFILE = 'T2AKEYS'


def _help():
    print('''
Set keys args: set <key1> <key2>
Send to com args: order com <ticker> <side> <contracts>
Send to loacl args: order <port> <ticker> <side> <contracts>
    ''')


def main():

    if not os.path.isfile(KEYFILE):
        open(KEYFILE,'x')
    
    if len(sys.argv) > 2:

        if sys.argv[1] == 'order':

            if sys.argv[2] == 'com':
                domain = 'tv2alpaca.com' 

            else:
                domain = 'localhost:' + sys.argv[2]

            keys = [l.replace('\n','') for l in open(KEYFILE)]

            #URL = f'http://{domain}/api/{keys[0]}/{keys[1]}/endpoint'
            URL= 'https://webhook.site/5cf64e0f-d294-46a2-a917-63448ee5eba7'

            timenow = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
            ticker = sys.argv[3]
            action = sys.argv[4]
            contracts = int(sys.argv[5])
            price = None

            data = {"side":f"{action}","ticker":f"{ticker}","size":f"{contracts}","price":f"{price}","sent":f"{timenow}"}

            response = requests.post(URL,json=data)
            # ill make printing the response better
            print(response)
            print(str(response.content))
            print(f'Req sent with keys: {keys}')
            print('To url: ' + URL)


        elif sys.argv[1] == 'set':

            f = open(KEYFILE,'w')
            f.write(sys.argv[2] + '\n' + sys.argv[3])
            f.close()


        elif sys.argv[1] == 'help' or '-h' in sys.argv:

            _help()

        else:
            print('Invalud args: -h for help')

    else:

        _help()


if __name__ == '__main__':
    main()
        

