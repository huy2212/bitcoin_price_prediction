import os
import pandas as pd
from binance.client import Client
from datetime import date

today = str(date.today())

def get_raw_data():
   api_key = os.environ.get('binance_api')
   api_secret = os.environ.get('binance_secret')
   client = Client(api_key, api_secret)   
   data = client.get_historical_klines('BTCUSDT', '1d', end_str = today, limit = 365)
   return data
   
def data_processing(data):
   for line in data:
      del line[1:3]
      del line[2:]
   btc_df = pd.DataFrame(data, columns=['date', 'close'])
   btc_df['close'] = btc_df['close'].astype('float32')
   btc_df['date'] = pd.to_datetime(btc_df['date'], unit='ms')
   btc_df['date'] = btc_df['date'].astype("string")
   return btc_df