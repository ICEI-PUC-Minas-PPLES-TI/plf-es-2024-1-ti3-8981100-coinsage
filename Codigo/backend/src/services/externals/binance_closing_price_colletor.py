import threading
import time

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
