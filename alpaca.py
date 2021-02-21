#!/usr/bin/env python3

import alpaca_trade_api as tradeAPI
import pandas as pd

class brokerage():
    
    def __init__(self, keyID, secretKey, baseURL = 'https://paper-api.alpaca.markets'):
        self.api = tradeAPI.REST(base_url=baseURL, key_id=keyID, secret_key=secretKey)
        self.account = self.api.get_account()
        self.clock = self.api.get_clock()
        self.portfolio = self.api.list_positions()
        self.orders = self.api.list_orders()

    def execBUY(self, ticker, qty, _type='market', timeInForce='gtc'):
        self.api.submit_order(symbol=ticker,qty=qty,side='buy',type=_type,time_in_force=timeInForce)

    def execSELL(self, ticker, qty, _type='market', timeInForce='gtc'):
        self.api.submit_order(symbol=ticker,qty=qty,side='sell',type=_type,time_in_force=timeInForce)

    def isAccountBlocked(self):
        return True if self.account.trading_blocked else False

    def isMarketOpen(self):
        return self.clock.is_open

    def getEquity(self):
        balanceChange = float(self.account.equity) - float(self.account.last_equity)
        return self.account.equity, balanceChange

    def getBuyingPower(self):
        return float(self.account.buying_power)

    def getPositions(self):
        positions = dict()
        for position in self.portfolio:
            positions[position.symbol] = position.qty
        return positions


    def getPosValue(self):
        value = 0
        for position in self.portfolio:
            value += float(position.market_value)
        return value

    def listOrders(self):
        return self.orders

    def cancelOrder(self,ID):
        self.api.cancel_order(ID)


    def getBarSet(self,ticker,interval='1Min',rows=200):
        barSet = self.api.get_barset(ticker,interval,rows)
        dfRaw = [ [] for _ in range(6) ]
        for bar in barSet[ticker] :
            row = [bar.t,bar.o,bar.h,bar.l,bar.c,bar.v]
            for i in range(0,6):
                dfRaw[i].append(row[i])
        headers = ['Time','Open','High','Low','Close','Volume']
        data = dict()
        for header,i in zip(headers,range(0,6)):
            data[header] = dfRaw[i]
        df = pd.DataFrame(data)
        df = df.set_index(headers[0])
        return df

