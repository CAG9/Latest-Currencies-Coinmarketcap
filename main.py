from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from coinbase_key import KEY 
import datetime
from datetime import date, timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def getdata(URL, KEY):
    parameters = {
        'start':'1',
        'limit':'5000',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(URL, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def createdataframe(columns):
    df = pd.DataFrame(columns = columns)
    return df
  
def transform(data):
    df = createdataframe(['coin','date','total_supply'])
    today = date.today()
    yesterday = str(today - timedelta(days = 1))
    yesterday_datetime = datetime.datetime.strptime(yesterday, '%Y-%m-%d')
    for coin in data['data']:
        symbol = coin['symbol']
        total_supply = coin['total_supply']
        date_added_str = coin['date_added'][:10]
        date_added = datetime.datetime.strptime(date_added_str, '%Y-%m-%d')
        if yesterday_datetime < date_added:
            df = df.append({'coin' : symbol, 'date' : date_added, 'total_supply' : total_supply},ignore_index = True)
        else:
            pass
    return df

def plot(data):
    data.sort_values(by=['total_supply'], ascending = False, inplace = True)
    plt.figure(figsize=(12, 8), dpi=80)
    sns.barplot(data=data, x = 'coin', y = 'total_supply')
    plt.title('Latest coin added to coinmarketcap')
    plt.xlabel('Coin',)
    plt.ylabel('Total Supply')
    plt.show()





if __name__ == "__main__":

    URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    raw_data = getdata(URL, KEY)
    if type(raw_data) == dict:
        data = transform(raw_data)
        plot(data)
    
    else:
        print(raw_data)


























