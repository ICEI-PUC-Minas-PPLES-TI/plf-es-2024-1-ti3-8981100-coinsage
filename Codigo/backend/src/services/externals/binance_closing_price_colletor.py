import threading
import time

from binance.spot import Spot
from loguru import logger


class BinanceClosingPriceColletor:
    def __init__(self):
        self.DEFAULT_QUOTE_ASSET = "USDT"
        self.coins_closing_prices = []
        self.NUMBER_THREDS = 3

    def collect(self, symbols: list[str], interval: str, limit: int):
        chunk_size = (len(symbols) + self.NUMBER_THREDS - 1) // self.NUMBER_THREDS
        threads = []
        results = []

        star_time = time.time()

        for i in range(self.NUMBER_THREDS):
            start_index = i * chunk_size
            end_index = min((i + 1) * chunk_size, len(symbols))
            chunk = symbols[start_index:end_index]

            thread = threading.Thread(target=lambda: results.extend(self.fetch_data(chunk, interval, limit)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        logger.info(f"Collecting {len(symbols)} cypto closing price from Binance took {(time.time() - star_time)}h")

        return results

    def fetch_data(self, coins, interval: str, limit: int):
        start_time = time.time()
        data = []
        for coin in coins:
            symbol = coin + self.DEFAULT_QUOTE_ASSET
            try:
                raw_data = Spot().klines(symbol=symbol, interval=interval, limit=limit)
            except:
                time.sleep(0.1)
                raw_data = Spot().klines(symbol=symbol, interval=interval, limit=limit)
            data.append({"symbol": coin, "data": raw_data})

        logger.info(f"Collecting {len(coins)} cypto closing price from DB took {(time.time() - start_time)}h")
        return data
