import threading
import time
from datetime import datetime
from typing import Any, List

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
        self.raws = {}
        self.times_called = 0

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

                session.commit()
            except Exception as err:
                logger.error(f"Error while calculating ema_8 for {result['symbol']}: {err}")

    def extract_data_sets(self, raw) -> tuple:
        try:
            ema8 = raw["ema8"]
        except:
            logger.info("No EM8 data from parameter.")
            ema8 = None
        try:
            ema21 = raw["ema21"]
        except:
            logger.info("No EM21 data from parameter.")
            ema21 = None
        try:
            ema50 = raw["ema50"]
        except:
            logger.info("No EM50 data from parameter.")
            ema50 = None
        try:
            ema200 = raw["ema200"]
        except:
            logger.info("No EM200 data from parameter.")
            ema200 = None

        return ema8, ema21, ema50, ema200

    def _fetch_calculate_emas(self, symbols: List[CurrencyBaseInfoModel], emas_raws: tuple) -> pandas.DataFrame:
        threads = []
        results = []

        if not emas_raws[0]:
            results.extend(self.calculate(symbols, timeframe="1d", ema_size=8))

        if not emas_raws[1]:
            thread = threading.Thread(
                target=lambda: results.extend(self.calculate(symbols, timeframe="1d", ema_size=21))
            )
            threads.append(thread)
            thread.start()
        if not emas_raws[2]:
            thread = threading.Thread(
                target=lambda: results.extend(self.calculate(symbols, timeframe="1d", ema_size=50))
            )
            threads.append(thread)
            thread.start()
        if not emas_raws[3]:
            thread = threading.Thread(
                target=lambda: results.extend(self.calculate(symbols, timeframe="1d", ema_size=200))
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    def _merge_ema_values(self, results: List[dict]) -> pandas.DataFrame:
        merged_values = pandas.DataFrame()

        for result in results:
            merged_values["symbol"] = result["symbol"]
            merged_values["closing_price"] = result["ema_values"]["close"]
            merged_values["open_price"] = result["ema_values"]["open"]
            merged_values["date"] = result["ema_values"]["time"]
            merged_values[f'ema_{result["ema_size"]}'] = result["ema_values"][f'ema_{result["ema_size"]}']

        merged_values["8_above_21"] = (merged_values["ema_8"] >= merged_values["ema_21"]).fillna(0).astype(int)
        merged_values["21_above_50"] = (merged_values["ema_21"] >= merged_values["ema_50"]).fillna(0).astype(int)
        merged_values["50_above_200"] = (merged_values["ema_50"] >= merged_values["ema_200"]).fillna(0).astype(int)

        return merged_values

    def _save_emas_aligned_on_db(
        self,
        session: Session,
        symbols: List[CurrencyBaseInfoModel],
        analysis_uuid: UUID,
        merged_values: pandas.DataFrame,
    ):
        for symbol in symbols:
            try:
                current_analysis = self.repository.get_by_symbol_str(session, symbol.symbol, analysis_uuid)

                if current_analysis is None:
                    logger.warning(f"Analysis not found for {symbol.symbol} - {analysis_uuid}")
                    continue

                ema8_above_21_all = merged_values["8_above_21"].tail(1).values[0] == 1
                ema21_above_50_all = merged_values["21_above_50"].tail(1).values[0] == 1
                ema50_above_200_all = merged_values["50_above_200"].tail(1).values[0] == 1

                emas_aligned = ema8_above_21_all and ema21_above_50_all and ema50_above_200_all
                current_analysis.ema_aligned = emas_aligned
                session.commit()
            except Exception as err:
                logger.error(f"Error while calculating ema crossovers for {symbol.symbol}: {err}")

    @show_runtime
    def calculate_crossovers(
        self, session: Session, symbols: List[CurrencyBaseInfoModel], analysis_uuid: UUID, raw=None
    ):
        """
        Calculates the EMA crossovers for a list of symbols.

        Args:
            session (Session): The database session.
            symbols (List[CurrencyBaseInfoModel]): The list of symbols to calculate the EMA crossovers for.
            analysis_uuid (UUID): The UUID of the analysis.
            raw (Optional[dict]): The dictionary containing the EMA values to use for calculation.

        Returns:
            pandas.DataFrame: The merged values of the EMA crossovers.
        """

        logger.info(
            f"Starting ema crossovers calculation for {len(symbols)} symbols at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        ema8, ema21, ema50, ema200 = self.extract_data_sets(raw)

        results = self._fetch_calculate_emas(symbols, (ema8, ema21, ema50, ema200))

        merged_values = self._merge_ema_values(results)

        self._save_emas_aligned_on_db(session, symbols, analysis_uuid, merged_values)

        return merged_values

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

        logger.info(f"Calculating EMA{ema_size} for {len(symbols)} symbols.")

        if len(symbols) >= self.NUMBER_THREDS:
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

        return self.fetch_data(symbols, timeframe, ema_size)

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

            data.append(
                {
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "ema_size": ema_size,
                    "ema_values": dict_data,
                }
            )

        return data

    def calc_ema(self, raw_data, ema_size: int) -> pandas.DataFrame:
        dataframe = pandas.DataFrame(raw_data)
        ema_name = f"ema_{ema_size}"

        # Calculate the initial mean for the first ema_size rows
        initial_mean = dataframe["close"].rolling(window=ema_size, min_periods=ema_size).mean()

        # Use rolling window to calculate EMA
        dataframe[ema_name] = dataframe["close"].ewm(span=ema_size, adjust=False).mean()

        # Fill NaN values with the initial mean
        dataframe[ema_name] = dataframe[ema_name].fillna(initial_mean)

        return dataframe

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
        if symbol not in self.raws:
            symbol_parsed = f"{symbol}USDT"
            self.times_called = self.times_called + 1
            raw_data = self.binance_price_colletor.get_candlestick_data(
                symbol=symbol_parsed, timeframe=timeframe, qty=self.FIXED_QUANTITY, get_raw_data=False
            )

            self.raws[symbol] = raw_data
        else:
            raw_data = self.raws[symbol]

        return self.calc_ema(raw_data, ema_size)
