import concurrent.futures
import logging
import time
from datetime import datetime, timedelta
from decimal import Decimal

from binance.spot import Spot
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.schemas.analysis.second_stage_analysis import VariationPerSchema
from src.models.schemas.external.binance_symbols_collected import BinanceSymbolsCollected
from src.repository.crud import second_stage_repository
from src.services.externals.binance_price_at_timestamp import BinancePriceAtTimestampService
from src.services.externals.binance_symbol_colletor import BinanceSymbolCollector
from src.utilities.runtime import show_runtime

logger = logging.getLogger(__name__)


class VariationPer:
    def __init__(self, session: Session):
        self.session = session
        self.repository = second_stage_repository
        self.binance_symbol_collector = BinanceSymbolCollector()
        self.binance_price_at_timestamp = BinancePriceAtTimestampService()

    def collect_variation_price(self) -> list[VariationPerSchema]:
        all_symbols = self.binance_symbol_collector.get_symbols()
        dates_to_collect = self.dates_to_collect()
        variation_per_list = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            future_to_symbol = {
                executor.submit(self.process_symbol, symbol, dates_to_collect): symbol for symbol in all_symbols
            }
            for future in concurrent.futures.as_completed(future_to_symbol):
                variation_per_list.append(future.result())

        return self.variation_greater_bitcoin(variation_per_list, dates_to_collect)

    def process_symbol(self, symbol, dates_to_collect):
        symbol_data = {"symbol": symbol.base_asset}
        for date_info in dates_to_collect:
            date_key, days_back = list(date_info.items())[0]
            time.sleep(0.1)
            price = self.binance_price_at_timestamp.get_by_symbol(symbol.base_asset, days_back)
            symbol_data[date_key] = price

        current_price = Spot().ticker_price(symbol.symbol)
        symbol_data["current_price"] = Decimal(current_price["price"]) if current_price else None
        return self.extract_variation(symbol_data)

    def dates_to_collect(self) -> list[dict]:

        days = {
            "week_variation_per": 7,
            "month_variation_per": 30,
            "quarter_variation_per": 90,
            "semester_variation_per": 180,
            "year_variation_per": 360,
        }
        datetime_now = datetime.now()
        dates_to_collect = []

        for variation_per, day in days.items():
            dates_to_collect.append({variation_per: datetime_now - timedelta(day)})
        return dates_to_collect

    def extract_variation(self, symbol_data) -> list[VariationPerSchema]:
        current_price = symbol_data["current_price"]
        del symbol_data["current_price"]
        for key, value in symbol_data.items():
            if value and isinstance(value, Decimal) and current_price:
                symbol_data[key] = current_price - value

        return symbol_data

    @show_runtime
    def fetch_variation_price(self, analysis_identifier: Uuid) -> None:
        variation_price = self.collect_variation_price()
        self.repository.add_variation_analysis(
            db=self.session, variation_analysis_data=variation_price, analysis_indentifier=analysis_identifier
        )

    def variation_greater_bitcoin(self, symbol_data: list[VariationPerSchema], dates_to_collect: list[dict]):
        btc_asset = BinanceSymbolsCollected(symbol="BTCUSDT", base_asset="BTC", quote_asset="USDT")
        btc_variation = self.process_symbol(btc_asset, dates_to_collect)
        for data in symbol_data:
            if not data["year_variation_per"] or not data["semester_variation_per"]:
                data["variation_greater_bitcoin"] = False
                continue

            if (
                data["year_variation_per"] > btc_variation["year_variation_per"]
                and data["semester_variation_per"] > btc_variation["semester_variation_per"]
            ):
                data["variation_greater_bitcoin"] = True
            else:
                data["variation_greater_bitcoin"] = False
        return symbol_data
