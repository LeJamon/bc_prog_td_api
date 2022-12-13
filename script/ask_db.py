import sqlite3
conn = sqlite3.connect('kline.db')

c = conn.cursor()

for row in c.execute('''SELECT * FROM kline order by id'''):
    print(row)