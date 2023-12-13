"""
Made by Rdhirschel
"""

# Alpaca-py documentation: https://alpaca.markets/sdks/python/trading.html
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.trading.client import TradingClient, OrderRequest
from alpaca.trading.requests import GetOrdersRequest, GetAssetsRequest, AssetStatus
from alpaca.trading.enums import OrderSide, QueryOrderStatus
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.enums import AssetClass

# Python libraries
import datetime as dt
import statistics
import time
import random as rnd
import math
import os

# Constants
OSCILLATION_THRESHOLD = 10
MAX_QTY_TO_BUY = 50
MAX_BUY_ORDERS = 5
MAX_SELL_ORDERS = 5
MAX_SPEND_ON_BUY = 100
API_KEY = '<API_KEY>' 
API_SECRET = '<API_SECRET>'

def ShouldSell(prices, position):
    if float(position.qty) <= 0:
        return False

    symbol = position.symbol.replace("USD", "/USD")
    close_prices = [bar.close for bar in prices[symbol]]
    average_price = statistics.mean(close_prices)
    current_price = close_prices[-1]
    previous_price = close_prices[-2] if len(close_prices) > 1 else current_price

    profit_threshold = 1.1 * close_prices[0]  # Adjustable

    if (current_price > average_price and current_price >= profit_threshold) or current_price < previous_price:
        return True

    return False

def print_positions(positions):
    for position in positions:
        print(f"Symbol: {position.symbol}")
        print(f"Asset Class: {position.asset_class}")
        print(f"Average Entry Price: {position.avg_entry_price}")
        print(f"Current Price: {position.current_price}")
        print(f"Quantity: {position.qty}")
        print(f"Unrealized Profit/Loss: {position.unrealized_pl}")
        print(f"Unrealized Profit/Loss %: {position.unrealized_plpc}")
        print("---------------------------")

def ShouldBuy(prices, position):
    close_prices = [bar.close for bar in prices[position.symbol]]

    average_price = statistics.mean(close_prices)

    price_deviation = statistics.stdev(close_prices)
    current_price = close_prices[-1]

    if price_deviation > OSCILLATION_THRESHOLD:
        return False

    if current_price > average_price or average_price > MAX_SPEND_ON_BUY or current_price > MAX_SPEND_ON_BUY:
        return False

    if current_price < average_price:
        return True
    
    return False

client = CryptoHistoricalDataClient()
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
cash = float(trading_client.get_account().cash)

search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO, status= AssetStatus.ACTIVE)
all_assets = trading_client.get_all_assets(filter=search_params)
stocks = [asset for asset in all_assets if 'BTC' not in asset.symbol] # BTC doesn't work for some reason

# Log file
with open("log.txt", "a") as log_file, open("cash.txt", "a") as cash_file:
    iteration = 0
    while True:
        positions = trading_client.get_all_positions()

        for position in positions:
            stock = position.symbol
            current_time = dt.datetime.now()
            PositionRequest = CryptoBarsRequest(
                symbol_or_symbols=position.symbol.replace("USD", "/USD"),
                timeframe=TimeFrame.Hour,
                start_time=current_time - dt.timedelta(days=1),
                end_time=current_time
            )
            try:
                prices = client.get_crypto_bars(PositionRequest)
            except Exception as e:
                continue

            if ShouldSell(prices, position):
                order_request = OrderRequest(symbol=stock, qty=position.qty, side=OrderSide.SELL, type="market", time_in_force="gtc")
                try:
                    trading_client.submit_order(order_request)
                    log_file.write(f"Sold {position.qty} shares of {stock} for {prices[-1].close}\n")
                    log_file.flush()  # Flush the log file to update changes
                    cash += float(position.qty) * prices[-1].close 

                    positions = trading_client.get_all_positions()
                except Exception as e:
                    print(f"")

        if len(positions) >= MAX_BUY_ORDERS:
            print("Max buy orders reached:")
            print_positions(positions)
            time.sleep(10)
            continue

        stock = stocks[rnd.randint(0, len(stocks) - 1)]

        current_time = dt.datetime.now()

        request = CryptoBarsRequest(
            symbol_or_symbols=stock.symbol,
            timeframe=TimeFrame.Hour,
            start_time=current_time - dt.timedelta(days=1),
            end_time=current_time
        )
        prices = client.get_crypto_bars(request)

        if stock.tradable and ShouldBuy(prices, stock):
            bars = prices[stock.symbol]

            if bars:
                last_price = bars[-1].close
            else:
                continue

            qty_to_buy = min(math.floor(MAX_SPEND_ON_BUY / last_price), MAX_QTY_TO_BUY)

            if cash >= qty_to_buy * last_price:
                order_request = OrderRequest(symbol=stock.symbol, qty=qty_to_buy, side=OrderSide.BUY, type="market", time_in_force="gtc", paper=True)
                try:
                    trading_client.submit_order(order_request)
                    log_file.write(f"Bought {qty_to_buy} shares of {stock.symbol} for {last_price}\n")
                    log_file.flush()  # Flush the log file to update changes
                    cash -= qty_to_buy * last_price
                except Exception as e:
                    print(f"")
            else:
                print(f"Not enough cash to buy {qty_to_buy} shares of {stock.symbol}")

        if iteration % 10 == 0:
            cash_file.write(f"Iteration: {iteration}, Cash: {cash}\n")
            cash_file.flush()

        iteration += 1

    log_file.close()
    cash_file.close()
