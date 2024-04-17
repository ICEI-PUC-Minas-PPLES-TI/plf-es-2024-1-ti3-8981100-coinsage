import threading
import time

import pandas
from binance.spot import Spot
from loguru import logger

from src.utilities.runtime import show_runtime


class BinancePriceColletor:
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

    def fetch_data(self, coins, interval: str, limit: int):
        data = []
        for coin in coins:
            symbol = coin + self.DEFAULT_QUOTE_ASSET
            try:
                raw_data = self.get_candlestick_data(symbol, interval, limit)
            except:
                time.sleep(0.1)
                raw_data = self.get_candlestick_data(symbol, interval, limit)
            data.append({"symbol": coin, "data": raw_data})

        return data

    def get_candlestick_data(
        self, symbol: str, timeframe: str, qty: int, timeZone: str = "-03:00", get_raw_data: bool = True
    ) -> list[dict]:
        raw_data = Spot().klines(symbol=symbol, interval=timeframe, limit=qty, timeZone=timeZone)

        if get_raw_data:
            return raw_data

        converted_data = []
        for candle in raw_data:
            converted_candle = {
                "crypto": symbol,
                "time": pandas.to_datetime(candle[0], unit="ms"),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5]),
                "close_time": candle[6],
                "quote_asset_volume": float(candle[7]),
                "number_of_trades": int(candle[8]),
                "taker_buy_base_asset_volume": float(candle[9]),
                "taker_buy_quote_asset_volume": float(candle[10]),
            }
            converted_data.append(converted_candle)
        return converted_data
