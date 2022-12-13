import requests
import json
import pandas as pd 
import sqlite3
import  pprint
apiexo4 = "GET /api/v3/uiKlines"

apiOpenOrder = "POST /api/v3/order (HMAC SHA256)"
apiCancelOrder = "DELETE /api/v3/order (HMAC SHA256)"

conn_kline = sqlite3.connect('kline.db')
c = conn_kline.cursor()

base_url = "https://api.binance.com"
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

def refreshData(_symbol): 
    response = requests.get("https://api.binance.com/api/v3/trades",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results)


refreshData("BTCUSDT")
