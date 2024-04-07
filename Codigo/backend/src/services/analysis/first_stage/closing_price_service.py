from datetime import datetime

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.models.schemas.analysis.closing_price_entity import ClosingPriceResponse
from src.repository.crud import currency_info_repository, first_stage_repository
from src.services.externals.binance_closing_price_colletor import BinanceClosingPriceColletor


class ClosingPriceService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = first_stage_repository
        self.symbols_repository = currency_info_repository
        self.binance_closing_price_colletor = BinanceClosingPriceColletor()

    def _collect_binance_closing_prices(self, interval="1d", limit=7):
        symbols_str = [symbol.symbol for symbol in self.symbols_repository.get_cryptos(self.session)]
        return self.binance_closing_price_colletor.collect(symbols=symbols_str, interval=interval, limit=limit)

    def collect_current_price_at_timestamp(self, symbol: str, time_to_collect_price: datetime):
        current_price = self.binance_closing_price_colletor.get_price_at_timestamp(symbol=symbol, timestamp=time_to_collect_price.timestamp)
        self.repository.update_current_price(self.session, symbol=symbol, current_price=current_price)

    def collect(self, analysis_indentifier: Uuid):
        start_time = datetime.now()

        closing_prices = self._collect_binance_closing_prices()
        closing_prices_models: list[FirstStageAnalysisModel] = []
        for closing_price in closing_prices:
            symbol = self.symbols_repository.get_currency_info_by_symbol(self.session, closing_price["symbol"])
            if symbol is None:
                logger.warning(f"Symbol {closing_price['symbol']} not found in DB")
                continue
            last_week = FirstStageAnalysisModel(
                uuid_analysis=analysis_indentifier,
                uuid_currency=symbol.uuid,
                closing_price=closing_price["data"][0][4],
                today=datetime.fromtimestamp(closing_price["data"][0][6] / 1000),  # Convert milliseconds to seconds
            )
            current_week = FirstStageAnalysisModel(
                uuid_analysis=analysis_indentifier,
                uuid_currency=symbol.uuid,
                closing_price=closing_price["data"][6][4],
                today=datetime.fromtimestamp(closing_price["data"][6][6] / 1000),  # Convert milliseconds to seconds
            )
            closing_prices_models.append(last_week)
            closing_prices_models.append(current_week)

        self.repository.save_all(self.session, closing_prices_models)

        logger.info(f"Collecting closing prices took {datetime.now() - start_time}h")

    def get_all_closing_prices(self):
        start_time = datetime.now()

        closing_prices = self.repository.get_all(self.session)
        closing_prices_responses = [
            ClosingPriceResponse(
                symbol=self.symbols_repository.get_currency_info_by_uuid(self.session, price.uuid_currency).symbol,
                closing_price=price.closing_price,
                week=price.today,
            )
            for price in closing_prices
        ]

        logger.info(f"Getting closing prices from DB took {datetime.now() - start_time}h")
        return closing_prices_responses

    def get_closing_price_by_symbol(self, symbol_str: str) -> list[FirstStageAnalysisModel]:
        symbol = self.symbols_repository.get_currency_info_by_symbol(self.session, symbol_str)
        if symbol is None:
            raise HTTPException(status_code=404, detail="Criptomoeda não encontrada")
        return self.repository.get_by_symbol(self.session, symbol)
