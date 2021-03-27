#!/usr/bin/env python3

#      __       ___         __
#     / /__   _|__ \ ____ _/ /___  ____ __________ _
#    / __/ | / /_/ // __ `/ / __ \/ __ `/ ___/ __ `/
#   / /_ | |/ / __// /_/ / / /_/ / /_/ / /__/ /_/ /
#   \__/ |___/____/\__,_/_/ .___/\__,_/\___/\__,_/
#                        /_/

# Written by Justus Languell <jus@gtsbr.org>, 2021

# algorithm.py - test shell for the order algorithm


from clint.textui import colored
import sys
from time import sleep

class alpaca:

    def __init__(self):
        self.poss = {}

    def getPos(self,ticker):

        if ticker in self.poss.keys():
            return int(self.poss[ticker])
        else:
            return 0

    def execBUY(self,ticker,size):
        
        if ticker in self.poss.keys():
            self.poss[ticker] += size
        else:
            self.poss[ticker] = size

        o = self.poss[ticker]
        print(colored.green(f'Buy order for {ticker} of {size} shares filled'))

    def execSELL(self,ticker,size):

        if ticker in self.poss.keys():
            self.poss[ticker] -= size
        else:
            self.poss[ticker] = -size

        o = self.poss[ticker]
        print(colored.red(f'Sell order for {ticker} of {size} shares filled'))

    def portfolio(self):
        print(colored.green('Portfolio'))
        for key in self.poss.keys():
            o = self.poss[key]
            stro = colored.green(o) if o >= 0 else colored.red(o)
            print(f'{key} : ' + stro)


def main():

    broker = alpaca()
    
    exit = False

    print(colored.green('Test shell for the order algorithm'))

    while exit == False:

        argv = input('>>> ')

        if argv != 'exit':

            argv = argv.split(' ')
            
            ticker = argv[1].upper()
            side = argv[0]
            abssize = int(argv[2])

            print(abssize)


            if side.upper() == 'BUY':
                size = abssize
            elif side.upper() == 'SELL':
                size = -abssize
            else:
                size = 0

            print(size)

            owned = broker.getPos(ticker.upper())

            conf = (owned*size < 0) 

            #print(f'ALREADY OWNED: {owned} shares')
            #print(f'REQUESTED SIZE: {size} shares')
          
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

            broker.portfolio()

        else:
            
            exit = True
            print(colored.red('Program exited'))



if __name__ == '__main__':

    main()
        






