#!/usr/bin/env python3

# Copyright (c) Justus Languell, 2020-2021 - All Rights Reserved
# Proprietary and Confidential
# Written by Justus Languell, jus@gtsbr.org, 2021

# WebHook format 
# {"side":"{{strategy.order.action}}","ticker":"{{ticker}}","size":"{{strategy.order.contracts}}","price":"{{strategy.order.price}}","sent":"{{timenow}}"}


import alpaca
from flask import Flask, render_template, request
import argparse
from time import sleep

app = Flask(__name__,template_folder='html')


@app.route('/')
def index():
    # Make this a render template
    return '''
    <style>code{font-size:140%;}</style>
    <h1>TradingView WebHook Routing API </h1> <h2 style="color:red;">ALPHA TEST</h2>
    <h2>The API is currently free to all, so please consider donating.</h2>
    <h3>Ethereum: <code>0xB1eDA5F757CF381d66dBd4ab867e69d217415759</code></h3>
    <h3>Copyright (c) <a href="https://www.gtsbr.org/">Justus Languell</a> 2021, All Rights Reserved</h3>
    '''

@app.route('/api/<key>/<scrt>/')
def account(key,scrt):
    broker = alpaca.brokerage(key,scrt)
    buyingPower = broker.getBuyingPower()
    return '<style>code{font-size:140%;}</style>\n' + f''' 
<h1>Alpaca Account</h1>
<h3>Key ID: <code>{key}</code></h3>
<h3>Secret Key: <code>{scrt}</code></h3>
<h3>Buying Power: <code>${buyingPower}</code></h3>
'''


@app.route('/api/<key>/<scrt>/endpoint',methods=['POST','GET'])
def reroute(key,scrt):
    if request.method == 'POST':
        hook = request.json
        authorized = True
        if authorized: 
            broker = alpaca.brokerage(key,scrt)
            positions = broker.getPositions()
            ticker = hook['ticker'].upper()
            side = hook['side'].upper()
            abssize = int(hook['size'])
    
            if side == 'BUY':
                size = abssize
            elif side == 'SELL':
                size = -abssize
            else:
                size = 0

            owned = int(positions[ticker])
            conf = (owned*size < 0) 

            if owned > 0 and size < 0:
                if abs(size) > owned:
                    broker.execSELL(ticker.upper(),owned)
                    sleep(.05)
                    broker.execSELL(ticker.upper(),abs(size+owned))
                elif abs(size) <= owned:
                    broker.execSELL(ticker.upper(),abs(size))
            if owned < 0 and size > 0:
                if size > abs(owned):
                    broker.execBUY(ticker.upper(),abs(owned))
                    sleep(.05)
                    broker.execBUY(ticker.upper(),size)
                if size < owned:
                    broker.execBUY(ticker.upper(),size)
            if owned > 0 and size > 0:
                broker.execBUY(ticker.upper(),size)
            if owned < 0 and size < 0:
                broker.execSELL(ticker.upper(),abs(size))
            
            if broker.getPositions()[ticker] == owned + size:
                return f'Success!'
            else:
                return f'[WARNING] An error may have occured!'
        else:
            return '',401 # Unauthorized
    else:
        return '',405 # Method not allowed


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d','--debug',help='Debug Mode',required=False,const='debug',nargs='?')
    if parser.parse_args().debug == 'debug':
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=80,debug=False)
