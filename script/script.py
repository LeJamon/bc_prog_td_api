import requests
import sqlite3
import  pprint
import hmac
import time
from hashlib import sha256
from urllib.parse import urlencode
from decouple import config

#set here your api key and secret key
api_key = config('your_api_key')
sec_key = config('your_sec_key')

#connect to data.db databse -> you should first have created the database by running create_database.py
conn = sqlite3.connect('data.db')
c = conn.cursor()

def GetCoin():
    response = requests.get("https://api.binance.com/api/v3/ticker/price")
    result = response.json()
    for r in result:
        print(r['symbol'])
        
def getDepth(direction, _symbol):
    response = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results[direction][0])


def orderBook(_symbol):
    response = requests.get("https://api.binance.com/api/v3/depth",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results)


def refreshDataCandleStick(_symbol, _duration):

    #open database connection
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    #call the binance api 
    response = requests.get("https://api.binance.com/api/v3/uiKlines",
        params=dict(symbol=_symbol, interval=_duration))
    results = response.json()
    pprint.pprint(results)

    #get the 500 last candle stick 
    print("Storing data in database")
    for i in range(len(results)):

        data=(_symbol, results[i][0])
        c.execute("SELECT * FROM kline WHERE pair=? AND date=?", data[:2])

        if not c.fetchone():
        #use ignore to avoid problem with the same id because id is based on the unix time
            c.execute("INSERT  INTO kline(pair, date,high,low,open,close,volume) VALUES(?,?,?,?,?,?,?)", 
            ( _symbol, results[i][0], results[i][2], results[i][3], results[i][1], results[i][4], results[i][5]))
            conn.commit()
    print("Done")

    #declare param for the trackning table
    c.execute("SELECT MAX(Id) from kline")
    last_id = c.fetchone()[0]
    exchange = "binance"
    table_name = 'kline'
    last_ckeck = int(time.time()*1000)

    c.execute("INSERT INTO tracking(exchange, trading_pair,duration,table_name,last_check,last_id) VALUES(?,?,?,?,?,?)", 
        (exchange, _symbol, _duration, table_name, last_ckeck,  last_id))
    conn.commit()

    c.close()
    conn.close()

def refreshDataTrade(_symbol): 

    #open database connection
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    #call binance api 
    response = requests.get("https://api.binance.com/api/v3/trades",
                 params=dict(symbol=_symbol))
    results = response.json()
    pprint.pprint(results)
    for i in range(len(results)):
        datalist = list(results[i].values())
        data=(_symbol, datalist[0])
        c.execute("SELECT * FROM trade WHERE traded_crypto=? AND uuid=?", data[:2])

        if not c.fetchone():
         #use ignore to avoid problem with the same id because id is based on the binance trade id
         # if buyer maker is false, it's a BUY, if true it's a SELL 
         
            c.execute("INSERT INTO trade(uuid, traded_crypto,price,created_at, side) VALUES(?,?,?,?,?)", 
            (datalist[0], _symbol, datalist[1], datalist[4], datalist[5]))
            conn.commit()
    print("done")

     #declare param for the trackning table
    c.execute("SELECT MAX(Id) from trade")
    last_id = c.fetchone()[0]
    exchange = "binance"
    table_name = 'trade'
    last_ckeck = int(time.time()*1000)
    _duration = 'none'

    #insert into tracking
    c.execute("INSERT INTO tracking(exchange, trading_pair,duration,table_name,last_check,last_id) VALUES(?,?,?,?,?,?)", 
        (exchange, _symbol, _duration, table_name, last_ckeck,  last_id))
    conn.commit()

    #close connection
    c.close()
    conn.close()



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



#main menu
def print_menu():
  print("1. Get all pairs listed on binance")
  print("2. Get the bid or ask on a pair")
  print("3. Get the orderbook on a pair")
  print("4. Get Klines of a pair and refresh the database") 
  print("5. Get the last trades and refresh the database") 
  print("6. Make a market order") 
  print("7. Make a Limit order")
  print("8. Delete an order") 
  print("9. Quit")
 
#Menu and option selection
def menu():
  while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
      print("\nYou selected option 1")
      GetCoin()

    elif choice == "2":
      print("\nYou selected option 2")
      direction = input("\nChoose the direction, bids or asks : ")
      pair = input("\nChoose the pair you want to look at eg BTCUSDT : ")
      getDepth(direction, pair)

    elif choice == "3":
      print("\nYou selected option 3")
      pair = input("\nChoose the pair you want to look at eg BTCUSDT : ")
      orderBook(pair)
   
    elif choice == "4":
      print("\nYou selected option 4")
      pair = input("\nChoose the pair you want to look at eg BTCUSDT : ")
      duration = input("\nChoose the duration of the candlestick eg 5m : ")
      refreshDataCandleStick(pair, duration)

    elif choice == "5":
      print("\nYou selected option 5")
      pair = input("\nChoose the pair you want to look at eg BTCUSDT : ")
      refreshDataTrade(pair)      

    elif choice == "6":
      print("\nYou selected option 6\n")
      pair = input("Choose the pair you want to trade at eg BTCUSDT : ")
      side = input("\nChoose the side eg BUY or SELL : ")
      quantity = input("\nChoose how many crypto you want to trade : ")
      makeMarketOrder(pair, side, quantity)
    
    elif choice == "7":  
      print("\nYou selected option 7\n")
      pair = input("Choose the pair you want to trade at eg BTCUSDT : ")
      side = input("Choose the side eg BUY or SELL : ")
      quantity = input("Choose how many crypto you want to trade : ")
      price = input("Choose the price for your order : ")
      makeLimitOrder(pair, side, quantity, price)
    
    elif choice == "8":
      print("\nYou selected option 8\n")
      orderId = input("Choose the Id of the order you want to cancel")
      cancelOrder(orderId)

    elif choice == "9":
      break
    else:
      print("\nInvalid choice. Please try again.\n")
    print("")

menu()