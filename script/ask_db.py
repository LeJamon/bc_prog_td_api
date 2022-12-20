import sqlite3

def ask_kline(): 
    conn= sqlite3.connect('kline.db')
    c= conn.cursor()
    for row in c.execute('''SELECT * FROM kline order by id'''):
        print(row)

def ask_trade(): 
    conn= sqlite3.connect('trade.db')
    c= conn.cursor()
    for row in c.execute('''SELECT * FROM trade order by id'''):
        print(row)