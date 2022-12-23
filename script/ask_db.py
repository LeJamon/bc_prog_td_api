import sqlite3

def ask_kline(): 
    conn= sqlite3.connect('data.db')
    c= conn.cursor()
    for row in c.execute('''SELECT * FROM kline order by id'''):
        print(row)

def ask_trade(): 
    conn= sqlite3.connect('data.db')
    c= conn.cursor()
    for row in c.execute('''SELECT * FROM trade order by id'''):
        print(row)

def ask_tracking(): 
    conn= sqlite3.connect('data.db')
    c= conn.cursor()
    for row in c.execute('''SELECT * FROM tracking order by Id'''):
        print(row)


def print_menu():
  print("1. Ask kline table")
  print("2. Ask trade table")
  print("3. Ask tracking table")
  print("4. Quit")
 
def menu():
  while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
      print("You selected option 1")
      ask_kline()

    elif choice == "2":
      print("You selected option 2")
      ask_trade()

    elif choice == "3":
      print("You selected option 3")
      ask_tracking()

    elif choice == "4":
      break
    else:
      print("Invalid choice. Please try again.")
    print("")

menu()