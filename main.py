from Classes.AlpacaController import AlpacaController
from pprint import pprint
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os

load_dotenv()

api_key = os.environ['ALPACA_API_KEY']
secret_key = os.environ['ALPACA_SECRET_KEY']


alpaca = AlpacaController(api_key, secret_key)

latest_data = alpaca.get_latest_shares_data(['SPY', 'GLD'])
print(latest_data['SPY'])

# bars_data = alpaca.get_historical_data(['SPY'], 100)

# print(bars_data)
# bars_data.to_csv('historicSPYCandleData.csv', index=True)
# account_data = alpaca.get_account()
# pprint(account_data)

# available_assets = alpaca.get_available_assets()
# pprint(available_assets[0].__dict__['symbol'])
# for item in available_assets[0]:
#     pprint(item)

# buy_shares = alpaca.buy_shares('SPY', 1)
# pprint(buy_shares)

# sell_shares = alpaca.buy_shares('SPY', 1)
# pprint(sell_shares)
