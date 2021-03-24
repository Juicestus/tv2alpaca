#!/usr/bin/env python3

# Written by Justus Languell <jus@gtsbr.org>, 2021

import alpaca 

from clint.textui import colored
from flask import Flask, render_template, request
import logging
import argparse
from time import sleep
import os
from datetime import datetime
import sys

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

hookFormat = '{"side":"{{strategy.order.action}}","ticker":"{{ticker}}","size":"{{strategy.order.contracts}}","price":"{{strategy.order.price}}","sent":"{{timenow}}"}'

logs = {}

def lprint(text,key):
    
    time = datetime.now().strftime('%m/%d/%Y @ %H:%M:%S')

    print(text)

    f = open('logfile','a')
    
    dels = ['[',']',key,'|','\n',':','—',' ORDER ']

    f.write(time+('&nbsp;'*8)+text+'\n')
    f.close()

    for d in dels:
        text = text.replace(d,'')

    if key not in logs.keys():
        logs[key] = [(time,text)]

    else:
        logs[key].append((time,text))


@app.route('/')
def index():

    return render_template('index.html',fmrt=hookFormat)


@app.route('/log')
def systemlog():

    content = ''.join([l+'<br>' for l in open('logfile','r')])

    return f'''
<h1>System Terminal STDOUT</h1>
<div style="
border:8px solid #ccc;
background-color:black;
padding:15px;">
<code style="
font-size:140%;
color:white;">{
content}
</code>
</div>'''


@app.route('/api/<key>/<scrt>/log',methods=['GET'])
def displaylog(key,scrt):
    
    if key in logs.keys():
        return render_template('log.html',name=key,logs=logs[key])
    else:
        return '<h2>Log not found</h2>'


@app.route('/api/<key>/<scrt>/endpoint',methods=['POST'])
def route(key,scrt):

    lprint('—— ORDER '+('—'*(os.get_terminal_size().columns-9)),key)
    lprint(f'|{key}|: [ACCEPTED]',key)

    if request.method == 'POST':

        hook = request.json
        
        # DEBUG ONLY
        print(hook)

        authorized = True

        if authorized: 

            lprint(f'|{key}|: [AUTHORIZED]',key)

            ticker = hook['ticker'].upper()
            side = hook['side'].upper()
            abssize = int(hook['size'])

            lprint(f'|{key}|: Order: {side} {ticker} x {abssize}',key)

            valid = True

            try:
                broker = alpaca.brokerage(key,scrt)

            except:
                valid = False

            if valid:

                positions = broker.getPositions()

                if broker.isMarketOpen():

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

                    lprint(f'|{key}|: ALREADY OWNED: {owned} shares',key)
                    lprint(f'|{key}|: REQUESTED SIZE: {size} shares',key)
                  
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
                        lprint(f'|{key}|: [SUCCESS] Guaranteed Success!\n',key)
                        return f'[SUCCESS] Success!'

                    else:
                        lprint(f'|{key}|: [SUCCESS] Unclear Success!?\n',key)
                        return f'[WARNING] An error may have occured!'

                else:
                    lprint(f'|{key}|: [WARNING] Market not open!\n',key)
                    return f'[WARNING] Market not open!'

            else:
                lprint(f'|{key}|: [ERROR] Key and secret not valid!\n',key)
                return f'[ERROR] Key and secret not valid!'

        else:
            lprint(f'|{key}|: [ERROR] UnAuthorized!\n',key)
            return '',401 

    else:
        lprint(f'|{key}|: [ERROR] Method not Allowed!\n',key)
        return '',405 


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '-d',
        '--debug',
        help='Debug Mode',
        required=False,
        const='debug',
        nargs='?'
    )

    if parser.parse_args().debug == 'debug':
        app.run(debug=True)

    else:
        app.run(host='0.0.0.0', port=80,debug=False)
