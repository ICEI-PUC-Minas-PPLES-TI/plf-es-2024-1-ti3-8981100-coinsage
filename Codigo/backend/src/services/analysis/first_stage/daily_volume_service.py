import logging
import re
from concurrent.futures import as_completed, ThreadPoolExecutor
from datetime import datetime
from typing import List

from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.schemas.analysis.first_stage_analysis import VolumeAnalysis
from src.repository.crud import first_stage_repository
from src.services.externals.binance_closing_price_colletor import BinanceClosingPriceColletor
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.utilities.runtime import show_runtime

logger = logging.getLogger(__name__)


class DailyVolumeService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = first_stage_repository
        self.binance_closing_price_colletor = BinanceClosingPriceColletor()
        self.binance_symbol_collector = BinanceSymbolCollector()

    def get_today_volume(self) -> list:
        rolling_window_size = []
        all_symbols = self.binance_symbol_collector.get_symbols()
        splited_symbols_list = self._split_symbol_list(all_symbols=all_symbols)

        for symbols in splited_symbols_list:
            window_price = self.binance_closing_price_colletor.get_rolling_window_price(symbols=symbols)
            for crypto in window_price:
                rolling_window_size.append({"symbol": crypto["symbol"], "today_volume": crypto["quoteVolume"]})
        return rolling_window_size

    def get_last_volume_valuation(self, today_volume: list) -> list:
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_volume = {executor.submit(self.process_volume, volume): volume for volume in today_volume}

            for future in as_completed(future_to_volume):
                volume = future_to_volume[future]
                try:
                    updated_volume = future.result()
                    results.append(updated_volume)
                except Exception as exc:
                    logger.error(f"Failed to process volume for symbol {volume['symbol']}: {exc}")

        logger.info("The valuation volumes were collected successfully.")
        return results

    def process_volume(self, volume):
        day = 1
        asset_info = self.binance_closing_price_colletor.get_rolling_window_price(
            symbols=[volume["symbol"]], window_size="{day}d".format(day=day)
        )

        while not asset_info[0]["volume"] > volume["today_volume"]:
            day += 1
            if day > 7:
                day = 1
                volume.update({"increase_volume": None, "increase_volume_day": None})
                logger.info(f"In the last week the symbol: {volume['symbol']} didn't appreciate.")
                return volume
            asset_info = self.binance_closing_price_colletor.get_rolling_window_price(
                symbols=[volume["symbol"]], window_size="{day}d".format(day=day)
            )
        volume.update(
            {"increase_volume": asset_info[0]["quoteVolume"], "increase_volume_day": asset_info[0]["closeTime"]}
        )
        return volume

    def get_volume_before_increase(self, increase_valuation_percentage: list) -> list:
        results = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_volume = {
                executor.submit(self.process_volume_before_increase, volume): volume
                for volume in increase_valuation_percentage
            }

            for future in as_completed(future_to_volume):
                volume = future_to_volume[future]
                try:
                    updated_volume = future.result()
                    results.append(updated_volume)
                except Exception as exc:
                    logger.error(f"Failed to process volume for symbol {volume['symbol']}: {exc}")

        return results

    def process_volume_before_increase(self, volume):
        increase_volume_day = volume["increase_volume_day"]
        if not increase_volume_day:
            volume.update({"volume_before_increase": None})
            return volume

        delta_date = datetime.now() - datetime.fromtimestamp(increase_volume_day / 1000)
        day = delta_date.days + 1
        if day == 8:
            logging.info(f"The symbol {volume['symbol']} has no day before valuation")
            volume.update({"volume_before_increase": None})
            return volume

        volume_before_increase = self.binance_closing_price_colletor.get_rolling_window_price(
            symbols=[volume["symbol"]], window_size="{day}d".format(day=day)
        )
        if not volume_before_increase:
            volume.update({"volume_before_increase": None})
            return volume

        volume.update({"volume_before_increase": volume_before_increase[0]["quoteVolume"]})
        return volume

    def get_increase_valuation_percentage(self, last_volume_valuation: list) -> list:
        for volume in last_volume_valuation:
            increase_percentage = self._calculate_valuation_percentage(volume)

            volume.update({"expressive_volume_increase": increase_percentage})

        return last_volume_valuation

    def _calculate_valuation_percentage(self, volume: dict) -> float:
        if not volume["increase_volume"]:
            return False
        increase_percentage = (float(volume["increase_volume"]) / float(volume["today_volume"])) * 100
        return True if increase_percentage > 200 else False

    def _split_symbol_list(self, all_symbols: list) -> list:
        return [[symbol.symbol for symbol in all_symbols[i : i + 100]] for i in range(0, len(all_symbols), 100)]

    @show_runtime
    def fetch_volume_data(self, analysis_identifier: Uuid) -> None:
        today_volume = self.get_today_volume()
        last_volume_valuation = self.get_last_volume_valuation(today_volume)
        increase_valuation_percentage = self.get_increase_valuation_percentage(last_volume_valuation)
        volume_before_increase = self.get_volume_before_increase(increase_valuation_percentage)
        volume_analysis_data = self.parser_quote_asset(volume_before_increase)
        self.repository.add_volume_analysis(self.session, volume_analysis_data, analysis_identifier)

    def parser_quote_asset(self, volume_analysis: List[VolumeAnalysis]) -> List[VolumeAnalysis]:
        def remove_suffix(input_string):
            return re.sub(r"(BTC|USDT)$", "", input_string)

        for volume in volume_analysis:
            volume["symbol"] = remove_suffix(input_string=volume["symbol"])
            increase_volume_day = volume["increase_volume_day"]
            if increase_volume_day:
                volume["increase_volume_day"] = datetime.fromtimestamp(increase_volume_day / 1000)
        return volume_analysis
