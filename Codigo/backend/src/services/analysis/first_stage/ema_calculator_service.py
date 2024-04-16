import threading
import time
from datetime import datetime
from typing import List

import pandas
from loguru import logger
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.schemas.base import BaseSchemaModel
from src.repository.crud import first_stage_repository
from src.services.externals.binance_price_colletor import BinancePriceColletor
from src.utilities.runtime import show_runtime


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
        self.FIXED_QUANTITY = 1000
        self.NUMBER_THREDS = 3
        self.binance_price_colletor = BinancePriceColletor()
        self.repository = first_stage_repository

    @show_runtime
    def append_ema8_and_relations(
        self, session: Session, symbols: List[CurrencyBaseInfoModel], analysis_uuid: UUID
    ) -> None:
        logger.info(
            f"Starting ema_8 calculation for {len(symbols)} symbols at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        results = self.calculate(symbols, timeframe="1w", ema_size=8)
        for result in results:
            try:
                crypto = result["symbol"]
                current_analysis = self.repository.get_by_symbol_str(session, crypto, analysis_uuid)
                df = result["ema_values"]
                open_price = current_analysis.open_price  # type: ignore
                close_price = current_analysis.closing_price  # type: ignore
                ema8 = df.loc[df["crypto"] == f"{crypto}USDT", "ema_8"].tail(1).values[0]
                ema8_lower_than_close_week = ema8 < close_price
                ema8_greater_than_open_week = ema8 > open_price

                current_analysis.ema8 = ema8  # type: ignore
                current_analysis.ema8_greater_open = ema8_greater_than_open_week  # type: ignore
                current_analysis.ema8_less_close = ema8_lower_than_close_week  # type: ignore

                # logger.debug(f"EMA8 for {crypto} is {ema8}")
                # logger.debug(f"EMA8 is greater than open price: {ema8_greater_than_open_week}")
                # logger.debug(f"EMA8 is less than close price: {ema8_lower_than_close_week}")

                session.commit()
            except Exception as err:
                logger.error(f"Error while calculating ema_8 for {result['symbol']}: {err}")
                session.rollback()  # TODO: check need

    @show_runtime
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

            # logger.debug(type(dict_data))

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
