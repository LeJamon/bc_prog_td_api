import sqlite3
conn_kline = sqlite3.connect('kline.db')
conn_trade = sqlite3.connect('trade.db')


c_kline = conn_kline.cursor()
c_trade = conn_trade.cursor()


#sql_kline ='''CREATE TABLE KLINE(
#    Id INETGER PRIMARY KEY, 
#    date INT,
#    high REAL,
#    low REAL,
#    open REAL, 
#    close REAL, 
#    volume REAL
# )'''

sql_trade ='''CREATE TABLE TRADE(
   Id INETGER PRIMARY KEY, 
   uuid TEXT,
   traded_crypto REAL,
   price REAL,
   created_at_int INT, 
   side _TEXT 
)'''

c_trade.execute(sql_trade)