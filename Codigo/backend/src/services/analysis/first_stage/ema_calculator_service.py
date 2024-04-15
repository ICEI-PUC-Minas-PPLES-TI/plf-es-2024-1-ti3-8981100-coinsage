import threading
import time
from typing import List

import pandas
from loguru import logger

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.schemas.base import BaseSchemaModel
from src.services.externals.binance_price_colletor import BinancePriceColletor
from src.utilities.runtime import show_runtime


class EmaCalcReturn(BaseSchemaModel):
    symbol: str
    timeframe: str
    ema_size: int
    ema_values: List[pandas.DataFrame]

    class Config:
        arbitrary_types_allowed = True


class EmaCalculatorService:
    """
    A class that calculates Exponential Moving Average (EMA) for a given symbol, timeframe, and EMA size.

    Attributes:
        binance_price_colletor (BinancePriceColletor): An instance of the BinancePriceColletor class.
        FIXED_QUANTITY (int): The fixed quantity value.

    Methods:
        calc_generic(symbol: str, timeframe: str, ema_size: int) -> pandas.DataFrame:
            Calculates the EMA for the given symbol, timeframe, and EMA size.

    """

    def __init__(self):
        self.binance_price_colletor = BinancePriceColletor()
        self.FIXED_QUANTITY = 1000
        self.NUMBER_THREDS = 3

    def calculate(self, symbols: List[CurrencyBaseInfoModel], timeframe: str, ema_size: int) -> List[dict]:
        """
        Calculates the Exponential Moving Average (EMA) for the given symbols, timeframe, and EMA size.

        Args:
            symbols (List[CurrencyBaseInfoModel]): A list of CurrencyBaseInfoModel objects.
            timeframe (str): The timeframe for the candlestick data.
            ema_size (int): The size of the EMA.

        Returns:
            List[dict]: A list of dict objects.

        """
        chunk_size = (len(symbols) + self.NUMBER_THREDS - 1) // self.NUMBER_THREDS
        threads = []
        results: List[dict] = []

        for i in range(self.NUMBER_THREDS):
            start_index = i * chunk_size
            end_index = min((i + 1) * chunk_size, len(symbols))
            chunk = symbols[start_index:end_index]

            thread = threading.Thread(target=lambda: results.extend(self.fetch_data(chunk, timeframe, ema_size)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    @show_runtime
    def fetch_data(self, symbols: List[CurrencyBaseInfoModel], timeframe: str, ema_size: int) -> List[dict]:
        """
        Fetches the EMA data for the given symbols, timeframe, and EMA size.

        Args:
            symbols (List[CurrencyBaseInfoModel]): A list of CurrencyBaseInfoModel objects.
            timeframe (str): The timeframe for the candlestick data.
            ema_size (int): The size of the EMA.

        Returns:
            List[EmaCalcReturn]: A list of EmaCalcReturn objects.
        """

        data: List[dict] = []
        for coin in symbols:
            symbol = coin.symbol
            try:
                dict_data = self.calc_generic(symbol, timeframe, ema_size)  # type: ignore
            except:
                time.sleep(0.1)
                dict_data = self.calc_generic(symbol, timeframe, ema_size)  # type: ignore

            logger.debug(type(dict_data))

            data.append({"symbol": symbol, "timeframe": timeframe, "ema_size": ema_size, "ema_values": dict_data})

        return data

    def calc_generic(self, symbol: str, timeframe: str, ema_size: int) -> pandas.DataFrame:
        """
        Calculates the Exponential Moving Average (EMA) for the given symbol, timeframe, and EMA size.

        Args:
            symbol (str): The symbol for which to calculate the EMA.
            timeframe (str): The timeframe for the candlestick data.
            ema_size (int): The size of the EMA.

        Example:
            calc_generic('BTC', '1w', 21)
            calc_generic('ETH', '1d', 50)

        Returns:
            pandas.DataFrame: A DataFrame containing the EMA values.

        """
        symbol_parsed = f"{symbol}USDT"
        raw_data = self.binance_price_colletor.get_candlestick_data(
            symbol=symbol_parsed, timeframe=timeframe, qty=self.FIXED_QUANTITY, get_raw_data=False
        )
        dataframe = pandas.DataFrame(raw_data)
        ema_name = f"ema_{ema_size}"
        multiplier = 2 / (ema_size + 1)
        initial_mean = dataframe["close"].head(ema_size).mean()

        for i in range(len(dataframe)):
            if i == ema_size:
                dataframe.loc[i, ema_name] = initial_mean
            elif i > ema_size:
                ema_value = dataframe.loc[i, "close"] * multiplier + dataframe.loc[i - 1, ema_name] * (1 - multiplier)
                dataframe.loc[i, ema_name] = ema_value
            else:
                dataframe.loc[i, ema_name] = 0.00

        return dataframe
