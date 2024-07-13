from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest , StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, GetAssetsRequest
from alpaca.trading.enums import OrderSide, TimeInForce,  QueryOrderStatus, AssetClass

from datetime import datetime, timedelta

class AlpacaController:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        
    # First need to connect to alpaca
    def alpaca_login(self):
        pass
    # get current portfolio
    def get_account(self):
        trading_client = TradingClient(self.api_key, self.secret_key)
        account = trading_client.get_account()
        return account
    
    def get_available_assets(self):
        trading_client = TradingClient(self.api_key, self.secret_key)
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
        
        assets = trading_client.get_all_assets(search_params)
        return assets
    
    def get_all_orders(self, status, side):
        trading_client = TradingClient('api-key', 'secret-key', paper=True)
        
        match status:
            case 'open':
                order_status = QueryOrderStatus.OPEN
            case 'closed':
                order_status = QueryOrderStatus.CLOSED
            case _:
                order_status = QueryOrderStatus.ALL
        
        match side:
            case 'buy':
                order_side = OrderSide.BUY
            case 'sell':
                order_side = OrderSide.SELL
                
        # params to filter orders by
        request_params = GetOrdersRequest(
                            status=order_status,
                            side=order_side
                        )

        # orders that satisfy params
        orders = trading_client.get_orders(filter=request_params)
        
    # get chosen share data
    def get_latest_shares_data(self, ticker_list):
        # choose between single share, group or index
        stock_client = StockHistoricalDataClient(self.api_key, self.secret_key)
        if len(ticker_list) > 1:
            request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker_list)
        else:
            request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker_list[0])
            
        latest_quote = stock_client.get_stock_latest_quote(request_params)
        return latest_quote
    
    def get_historical_data(self, ticker_list, time_delta):
        stock_client = StockHistoricalDataClient(self.api_key, self.secret_key)
        print(f'start: {datetime.today() - timedelta(days=(time_delta +1))}')
        print(f'end: {datetime.today() - timedelta(days=time_delta)}')
        print(f'start: {timedelta(days=(time_delta +1))}')
        print(f'end: {timedelta(days=time_delta)}')
        request_params = StockBarsRequest(
                        symbol_or_symbols=ticker_list,
                        timeframe=TimeFrame.Minute,
                        start=datetime.today() - timedelta(days=(time_delta)),
                        end=datetime.today() - timedelta(hours=2)
                 )

        bars = stock_client.get_stock_bars(request_params)
        return bars.df
    # buy chosen share
    def buy_shares(self, ticker, amount ):
        trading_client = TradingClient(self.api_key, self.secret_key)
        # preparing orders
        market_order_data = MarketOrderRequest(
                    symbol=ticker,
                    qty=amount, # this can be fractional e.g. 0.5 etc.
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
        # Market order
        market_order = trading_client.submit_order(
                order_data=market_order_data
               )
        return market_order
    # sell share from portfolio
    def sell_shares(self, ticker, amount):
        trading_client = TradingClient(self.api_key, self.secret_key)
        # preparing orders
        market_order_data = MarketOrderRequest(
                    symbol=ticker,
                    qty=amount, # this can be fractional e.g. 0.5 etc.
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
        # Market order
        market_order = trading_client.submit_order(
                order_data=market_order_data
               )
        return market_order
    def attempt_order_cancel(self):
        trading_client = TradingClient('api-key', 'secret-key', paper=True)

        # attempt to cancel all open orders
        cancel_statuses = trading_client.cancel_orders()
        return cancel_statuses
        
