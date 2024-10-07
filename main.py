from Classes.AlpacaController import AlpacaController
from pprint import pprint
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import os
from datetime import datetime

load_dotenv()

print('test')

api_key = os.environ['ALPACA_API_KEY']
secret_key = os.environ['ALPACA_SECRET_KEY']
alpaca = AlpacaController(api_key, secret_key)

## Get Available Equity Assets
available_assets = alpaca.get_available_assets()

# Get 10 tickers worth of historical data with 100 days time delta.
ticker_list = ['SPY']

# Check if ticker tradeable
verified_tickers = [asset.symbol for asset in available_assets if asset.symbol in ticker_list and asset.tradable]

historical_ticker_data = alpaca.get_historical_data(verified_tickers, 100)

# Save data as csv
# historical_ticker_data.to_csv(f'Historical Bar Data.csv')

# Give that data to GPT with the template for it to return.
# Receive the template filled in and run validation check
# Calculate take profit and stop loss amounts based on plan.
# def take_stop_calculator(take_profit_percentage, stop_loss_percentage, purchase_price):
#     take_profit = purchase_price * (1+take_profit_percentage)
#     stop_loss = purchase_price * (1-stop_loss_percentage)
    
#     return take_profit, stop_loss

# print(take_stop_calculator(0.10, 0.02, 100))
# Set up timer to check
