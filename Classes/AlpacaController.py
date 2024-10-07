from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest , StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, GetAssetsRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce,  QueryOrderStatus, AssetClass, AssetStatus

from datetime import datetime, timedelta

class AlpacaController:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.trading_client = TradingClient(api_key, secret_key)
        self.stock_client = StockHistoricalDataClient(api_key, secret_key)
        
    # First need to connect to alpaca
    def alpaca_login(self):
        pass
    # get current portfolio
    def get_account(self):
        return self.trading_client.get_account()
    
    def get_available_assets(self):
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY, status=AssetStatus.ACTIVE)
        return self.trading_client.get_all_assets(search_params)
    
    def get_all_orders(self, status, side):
        status_map = {
            'open': QueryOrderStatus.OPEN,
            'closed': QueryOrderStatus.CLOSED
        }
        order_status = status_map.get(status, QueryOrderStatus.ALL)
        order_side = OrderSide.BUY if side == 'buy' else OrderSide.SELL

        request_params = GetOrdersRequest(
            status=order_status,
            side=order_side
        )
        return self.trading_client.get_orders(filter=request_params)
        
    # get chosen share data
    def get_latest_shares_data(self, ticker_list):
        # choose between single share, group or index
        request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker_list)
        return self.stock_client.get_stock_latest_quote(request_params)
    
    def get_historical_data(self, ticker_list, time_delta):
        start_date = datetime.today() - timedelta(days=time_delta)
        end_date = datetime.today() - timedelta(hours=2)

        request_params = StockBarsRequest(
            symbol_or_symbols=ticker_list,
            timeframe=TimeFrame.Minute,
            start=start_date,
            end=end_date
        )
        return self.stock_client.get_stock_bars(request_params).df
    
    # buy chosen share
    def buy_shares(self, ticker, amount):
        # preparing orders
        market_order_data = MarketOrderRequest(
                    symbol=ticker,
                    qty=amount, # this can be fractional e.g. 0.5 etc.
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
        # Market order
        return self.trading_client.submit_order(order_data=market_order_data)
    
    # sell share from portfolio
    def sell_shares(self, ticker, amount):
        # preparing orders
        market_order_data = MarketOrderRequest(
                    symbol=ticker,
                    qty=amount, # this can be fractional e.g. 0.5 etc.
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
        # Market order
        return self.trading_client.submit_order(order_data=market_order_data)
    
    def limit_buy_order(self, ticker, limit_price, take_profit, stop_loss):
        print('start')
        take_profit_request = TakeProfitRequest(limit_price=take_profit)
        stop_loss_request = StopLossRequest(stop_price=stop_loss)
        limit_order_data = LimitOrderRequest(
                    symbol=ticker,
                    limit_price=limit_price,
                    take_profit=take_profit_request,
                    stop_loss=stop_loss_request,
                    qty=1,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.FOK
                   )
        
        return self.trading_client.submit_order(order_data=limit_order_data)
    
    def limit_sell_order(self, ticker, limit_price, notional):
        limit_order_data = LimitOrderRequest(
                    symbol=ticker,
                    limit_price=limit_price,
                    notional=notional,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.FOK
                   )
        
        return self.trading_client.submit_order(order_data=limit_order_data)
    
    def attempt_order_cancel(self):
        # attempt to cancel all open orders
        return self.trading_client.cancel_orders()
        
    def get_all_positions(self):
        return self.trading_client.get_all_positions()
    
    def close_all_positions(self):
        return self.trading_client.close_all_positions(cancel_orders=False)
