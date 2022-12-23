import sqlite3
conn = sqlite3.connect('data.db')

#Simple script to create the database : data.db
#It creates 3 tables : kline, trade and tracking
#kline : store the kline data
#trade : store the trade data
#tracking : store the last id of the last kline/trade retrieved


c = conn.cursor()



sql_kline ='''CREATE TABLE kline(
    Id INTEGER PRIMARY KEY AUTOINCREMENT, 
    pair TEXT, 
    date INT,
    high REAL,
    low REAL,
    open REAL, 
    close REAL, 
    volume REAL
 )'''

sql_trade ='''CREATE TABLE trade(
   Id INTEGER PRIMARY KEY AUTOINCREMENT, 
   uuid TEXT, 
   traded_crypto TEXT,
   price REAL,
   created_at INT, 
   side TEXT
)'''

sql_update = '''CREATE TABLE tracking(
   Id INTEGER PRIMARY KEY AUTOINCREMENT, 
   exchange TEXT, 
   trading_pair TEXT,
   duration TEXT, 
   table_name TEXT, 
   last_check INT, 
   last_id INT
)'''

c.execute(sql_kline)
c.execute(sql_trade)
c.execute(sql_update)

c.close()
conn.close()