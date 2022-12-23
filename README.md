# Automating Trading - Binance - Python

This project is a continuation of the Blockchain programming courses offered at ESILV. The objective is to design a python application allowing the user to access a certain number of Binance services and information via API requests.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You should have on your computer :
- Python 3.6 or higher
- SqLite3

You shloud a Binance account and configure API keys. Check this [tutorial](https://www.binance.com/en-NZ/support/faq/how-to-create-api-360002502072).

### Installing

Clone this repo.  
Then navigate to the script folder. Verify that you have all the requirement and depedencies installed.  
In script.py, provide your Binance API key :
```
api_key = config('your_api_key')
sec_key = config('your_sec_key')
```
You can also configure it with a .env file.

### Run

First enter in you cmd :  
```
create_db.py
```  
This will generate and configure the database.

Then you can start the main script/console application :

```
script.py
```  

You will have access to a console menu and a bunch of options.

### Example with pictures 
![](https://ibb.co/sjW1MLt)
