#!/usr/bin/env python3

# Written by Justus Languell, jus@gtsbr.org, 2021
# http://ce13945d70eb.ngrok.io/api/PKF29LL614BD93L6NNDU/itebP7fQt3J2OgIwdTHyJjs9hTxqG5cAUmDZJcQD/endpoint

import alpaca
from flask import Flask, render_template, request
import argparse
from time import sleep

app = Flask(__name__,template_folder='html')
hookFormat = '{"side":"{{strategy.order.action}}","ticker":"{{ticker}}","size":"{{strategy.order.contracts}}","price":"{{strategy.order.price}}","sent":"{{timenow}}"}'

@app.route('/')
def index():
    return render_template('index.html',fmrt=hookFormat)

@app.route('/api/<key>/<scrt>/endpoint',methods=['POST'])
def reroute(key,scrt):
    if request.method == 'POST':
        hook = request.json
        authorized = True

        if authorized: 
            print(f'Incoiming Hook - RAW: {hook}')
            broker = alpaca.brokerage(key,scrt)
            if broker.isMarketOpen():

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
                try:
                    owned = int(positions[ticker])
                except:
                    owned = 0
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

                #try:
                #    owned = int(positions[ticker])
                #except:
                #    owned = 0 
                
                #if broker.getPositions()[ticker] == owned + size:
                print(broker.listOrders())
                return f'Success!'
                #else:
                #return f'[WARNING] An error may have occured!'
            else:
                return f'[WARNING] Market not open!'
        else:
            return '',401 
    else:
        return '',405 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d','--debug',help='Debug Mode',required=False,const='debug',nargs='?')
    if parser.parse_args().debug == 'debug':
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=80,debug=False)
