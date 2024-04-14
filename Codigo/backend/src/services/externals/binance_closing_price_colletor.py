import threading
import time
from datetime import datetime
from typing import Callable

from binance.spot import Spot
from loguru import logger

from src.utilities.runtime import show_runtime


class BinanceClosingPriceColletor:
    def __init__(self):
        self.DEFAULT_QUOTE_ASSET = "USDT"
        self.coins_closing_prices = []
        self.NUMBER_THREDS = 3

    @show_runtime
    def collect(self, symbols: list[str], interval: str, limit: int):
        chunk_size = (len(symbols) + self.NUMBER_THREDS - 1) // self.NUMBER_THREDS
        threads = []
        results = []

        for i in range(self.NUMBER_THREDS):
            start_index = i * chunk_size
            end_index = min((i + 1) * chunk_size, len(symbols))
            chunk = symbols[start_index:end_index]

            thread = threading.Thread(target=lambda: results.extend(self.fetch_data(chunk, interval, limit)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    @show_runtime
    def fetch_data(self, coins, interval: str, limit: int):
        data = []
        for coin in coins:
            symbol = coin + self.DEFAULT_QUOTE_ASSET
            try:
                raw_data = Spot().klines(symbol=symbol, interval=interval, limit=limit, timeZone="-03:00")
            except:
                time.sleep(0.1)
                raw_data = Spot().klines(symbol=symbol, interval=interval, limit=limit, timeZone="-03:00")
            data.append({"symbol": coin, "data": raw_data})

        return data

    def get_price_at_timestamp(self, symbol: str, timestamp: Callable[[], float]) -> float | None:
        """
        Retrieves the closing price of a cryptocurrency at a specific timestamp.

        Args:
            symbol (str): The symbol of the cryptocurrency pair.
            interval (str): The interval of the kline data.
            timestamp (int): The timestamp for which the closing price is to be retrieved.

        Returns:
            float or None: The closing price of the cryptocurrency at the specified timestamp,
            or None if the price could not be retrieved.

        Note:
            The timestamp should be in milliseconds since the Unix epoch."""
        try:
            raw_data = Spot().klines(symbol=symbol, interval="1m", startTime=timestamp, endTime=timestamp, limit=1)
            if raw_data:
                return float(raw_data[0][4])
        except Exception as e:
            logger.error(f"Error fetching price for {symbol} at timestamp {timestamp}: {e}")
        return None

    def get_rolling_window_price(self, symbols: list, window_size: str | None = None):
        try:
            rolling_window_price = Spot().rolling_window_ticker(symbols=symbols, windowSize=window_size)
            if rolling_window_price:
                return rolling_window_price
        except Exception as e:
            logger.error(f"Error to collect rolling window price: {e}")
        return None


str
