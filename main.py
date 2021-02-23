#!/usr/bin/env python3

# Written by Justus Languell, jus@gtsbr.org, 2021
# http://679a40ea7049.ngrok.io/api/PK87P8C3BAU1JDO4M3QR/XfgNN1ywesC70L4tz4HjAsfXCEdLD2em5dRkHPER/endpoint

import alpaca
from flask import Flask, render_template, request
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
import argparse
from time import sleep
import os

app = Flask(__name__,template_folder='html')
hookFormat = '{"side":"{{strategy.order.action}}","ticker":"{{ticker}}","size":"{{strategy.order.contracts}}","price":"{{strategy.order.price}}","sent":"{{timenow}}"}'

@app.route('/')
def index():
    return render_template('index.html',fmrt=hookFormat)

@app.route('/api/<key>/<scrt>/endpoint',methods=['POST'])
def reroute(key,scrt):
    width = os.get_terminal_size().columns-6
    print('-- ORDER '+('—'*(os.get_terminal_size().columns-9)))
    print(f'|{key}|: [ACCEPTED]')
    if request.method == 'POST':
        hook = request.json
        authorized = True

        if authorized: 
            print(f'|{key}|: [AUTHORIZED]')
            broker = alpaca.brokerage(key,scrt)
            if broker.isMarketOpen():
                positions = broker.getPositions()
                ticker = hook['ticker'].upper()
                side = hook['side'].upper()
                abssize = int(hook['size'])

                print(f'|{key}|: Order: {side} {ticker} x {abssize}')

                if side == 'BUY':
                    size = abssize
                elif side == 'SELL':
                    size = -abssize
                else:
                    size = 0
                try:
                    owned = int(positions[ticker])
                except:
                    owned = 0
                conf = (owned*size < 0) 

                print(f'|{key}|: ALREADY OWNED: {owned} shares')
                print(f'|{key}|: REQUESTED SIZE: {size} shares')

              
                if owned > 0 and size < 0:
                    if abs(size) > owned:
                        broker.execSELL(ticker.upper(),owned)
                        sleep(1)
                        broker.execSELL(ticker.upper(),abs(size+owned))
                    elif abs(size) <= owned:
                        broker.execSELL(ticker.upper(),abs(size))
                if owned < 0 and size > 0:
                    if size > abs(owned):
                        broker.execBUY(ticker.upper(),abs(owned))
                        sleep(1)
                        broker.execBUY(ticker.upper(),size+owned)
                    if size < owned:
                        broker.execBUY(ticker.upper(),size)
                if owned >= 0 and size > 0:
                    broker.execBUY(ticker.upper(),size)
                if owned <= 0 and size < 0:
                    broker.execSELL(ticker.upper(),abs(size))

                try:
                    nowOwned = int(positions[ticker])
                except:
                    nowOwned = 0 

                if nowOwned == owned + size:
                    print(f'|{key}|: [SUCCESS] Guaranteed Success!\n')
                    return f'[SUCCESS] Success!'
                else:
                    print(f'|{key}|: [SUCCESS] Unclear Success!?\n')
                    return f'[WARNING] An error may have occured!'
            else:
                print(f'|{key}|: [WARNING] Market not open!\n')
                return f'[WARNING] Market not open!'
        else:
            print(f'|{key}|: [ERROR] UnAuthorized!\n')
            return '',401 
    else:
        print(f'|{key}|: [ERROR] Method not Allowed!\n')
        return '',405 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d','--debug',help='Debug Mode',required=False,const='debug',nargs='?')
    if parser.parse_args().debug == 'debug':
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=80,debug=False)
