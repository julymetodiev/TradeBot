# Created by Miles Luders

import time
import math
import requests
import config
from hmac import new as _new
from urllib.parse import urlencode as _urlencode
from hashlib import sha512 as _sha512


class PoloniexWrapper:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
    
    def get_with_retry(self, url):
        data = None
        while data is None:
            try:
                data = requests.get(url)
            except requests.exceptions.ChunkedEncodingError as e:
                continue
        return data.json()
        
    def post_with_retry(self, payload):
        data = None
        while data is None:
            try:
                data = requests.post(**payload)
            except requests.exceptions.ChunkedEncodingError as e:
                continue
        return data.json()
                
    def private_command(self, args, timeout=30):
        date = None
        for _ in range(timeout):
            args['nonce'] = int(time.time()*10)
            sign = _new(
                self.api_secret.encode('utf-8'),
                _urlencode(args).encode('utf-8'),
                _sha512)
            headers = {
                'Key': self.api_key,
                'Sign': sign.hexdigest()
            } 
            payload = {
                'url': 'https://poloniex.com/tradingApi',
                'headers': headers,
                'data': args
            }

            data = self.post_with_retry(payload)
            if 'error' in data:
                print(data)
                data = None
                time.sleep(1)
                continue
            else:
                break;
        return data
        
    def get_ticker(self):
        return self.get_with_retry('https://poloniex.com/public?command=returnTicker')
        
    def get_order_book(self, pair, depth=30):
        base = "https://poloniex.com/public?command=returnOrderBook"
        pair = "&currencyPair=" + pair
        depth = "&depth=" + str(depth)
        url = base + pair + depth
        print(url)
        return self.get_with_retry(url)
        
        
    def get_chart_data(self, pair, period=300, days=60):
        base = 'https://poloniex.com/public?command=returnChartData'
        start = '&start=' + str(time.time()-(days*24*60*60))
        end = '&end=' + '9999999999'
        pair = '&currencyPair=' + pair
        period = '&period=' + str(period)
        url = base + pair + start + end + period
        return self.get_with_retry(url)
         
    def get_balances(self):
        args = {
            'command': 'returnBalances'
        }
        return self.private_command(args)
    
    def buy(self, pair, rate, amount):
        args = {
            'command': 'buy',
            'currencyPair': pair,
            'rate': rate,
            'amount': amount,
            'immediateOrCancel': 1
        }
        return self.private_command(args)
    
    def sell(self, pair, rate, amount):
        args = {
            'command': 'sell',
            'currencyPair': pair,
            'rate': rate,
            'amount': amount,
            'immediateOrCancel': 1
        }
        return self.private_command(args)
        
    
if __name__ == '__main__':
    p = PoloniexWrapper(config.POLONIEX_API_KEY, config.POLONIEX_API_SECRET)
    
    '''usdt_balance = float(p.get_balances()['USDT'])
    order_book = p.get_order_book('USDT_BTC')
    rate = float(order_book['asks'][5][0])
    amount = (usdt_balance / rate)
    
    print(usdt_balance)
    print(rate)
    print(amount)
    print(p.buy('USDT_BTC', rate, amount))'''
    
    
    '''btc_balance = float(p.get_balances()['BTC'])
    order_book = p.get_order_book('USDT_BTC')
    rate = float(order_book['bids'][5][0])
    amount = (btc_balance / rate)
    
    print(btc_balance)
    print(rate)
    print(amount)
    print(p.sell('USDT_BTC', rate, btc_balance))'''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    