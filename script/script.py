import requests
import pandas as pd 
import sqlite3
import  pprint
import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode
from decouple import config

api_key = config('api_key')
sec_key = config('sec_key')

conn_kline = sqlite3.connect('kline.db')
c = conn_kline.cursor()




def GetCoin():
    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    results = response.json()
    pprint.pprint(results)


def getDepth(direction, _symbol):
    response = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results[direction][0])


def orderBook(direction, _symbol):
    response = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results)


def refreshDataCandleStick(_symbol, _duration):

    #ajoputer un moyen de choper les valeurs plus récentes que la dernières en date
    response = requests.get("https://api.binance.com/api/v3/uiKlines",
        params=dict(symbol=_symbol, interval=_duration))
    results = response.json()
    
    #get the last kandle stick 
    
    for i in range(499):
        c.execute("INSERT INTO kline VALUES(?,?,?,?,?,?,?)",
        (results[i][0], results[i][0], results[i][2], results[i][3], results[i][1], results[i][4], results[i][5]))
        conn_kline.commit()


def refreshData(_symbol): #ajouter la partie database 
    response = requests.get("https://api.binance.com/api/v3/trades",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results)


def makeMarketOrder(_symbol,_side,_quantity):
    timestamp = int(time.time()*1000)
    
    header = {'X-MBX-APIKEY': api_key} 

    param = {'symbol': _symbol,
                'side': _side,
                'type': 'MARKET',
                'quantity': _quantity,
                'timestamp': timestamp
            } 

    query_string = urlencode(param)
    
    param['signature'] = hmac.new(key= sec_key.encode('utf-8'),msg=query_string.encode('utf-8'),digestmod=sha256).hexdigest()
    print(param['signature'])
    response = requests.post("https://api.binance.com/api/v3/order",headers=header, params=param)
    pprint.pprint(response.json())


def makeLimitOrder(_symbol, _side, _quantity,_price):

    timestamp = int(time.time()*1000)
    
    header = {'X-MBX-APIKEY': api_key} 

    param = {'symbol': _symbol,
                'side': _side,
                'type': 'LIMIT',
                'quantity': _quantity,
                'price': _price, 
                'timeInForce':'GTC',
                'timestamp': timestamp
            } 

    query_string = urlencode(param)
    
    param['signature'] = hmac.new(key= sec_key.encode('utf-8'),msg=query_string.encode('utf-8'),digestmod=sha256).hexdigest()
    print(param['signature'])
    response = requests.post("https://api.binance.com/api/v3/order",headers=header, params=param)
    pprint.pprint(response.json())


def cancelOrder(_symbol, _orderId):
    timestamp = int(time.time()*1000)
    header = {'X-MBX-APIKEY': api_key}
    param = {'symbol': _symbol,
                'orderId':_orderId,
                'timestamp': timestamp
            } 
    query_string = urlencode(param)
    param['signature'] = hmac.new(key= sec_key.encode('utf-8'),msg=query_string.encode('utf-8'),digestmod=sha256).hexdigest()
    response = requests.delete("https://api.binance.com/api/v3/order",headers=header, params=param)
    pprint.pprint(response.json())

makeMarketOrder('DOTBUSD','BUY','3')
