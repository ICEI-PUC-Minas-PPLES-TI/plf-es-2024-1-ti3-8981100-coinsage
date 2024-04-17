from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.models.schemas.analysis.closing_price_entity import PricesResponse
from src.models.schemas.analysis.first_stage_analysis import AnalysisCurrencyInfo, FirstStageAnalysisResponse
from src.models.schemas.sector import SectorRead
from src.repository.crud import currency_info_repository, first_stage_repository
from src.services.externals.binance_price_colletor import BinancePriceColletor
from src.services.sectors_info_collector import SectorsCollector
from src.utilities.runtime import show_runtime


class PriceService:
    """
    Collect: close, open prices
    """

    def __init__(self, session: Session):
        self.session = session
        self.repository = first_stage_repository
        self.symbols_repository = currency_info_repository
        self.sectors_service = SectorsCollector()
        self.binance_closing_price_colletor = BinancePriceColletor()

    def _collect_binance_closing_prices(self, interval="1d", limit=7):
        symbols_str = [symbol.symbol for symbol in self.symbols_repository.get_cryptos(self.session)]
        return self.binance_closing_price_colletor.collect(symbols=symbols_str, interval=interval, limit=limit)

    def collect_current_price_at_timestamp(self, symbol: str, time_to_collect_price: datetime):
        current_price = self.binance_closing_price_colletor.get_price_at_timestamp(
            symbol=symbol, timestamp=time_to_collect_price.timestamp
        )
        self.repository.update_current_price(self.session, symbol=symbol, current_price=current_price)

    def extract(self, analysis_indentifier: Uuid, prices):
        first_stage_models: list[FirstStageAnalysisModel] = []

        for price in prices:
            symbol = self.symbols_repository.get_currency_info_by_symbol(self.session, price["symbol"])

            if symbol is None:
                logger.warning(f"Symbol {price['symbol']} not found in DB")
                continue

            if len(price["data"]) != 7:
                logger.warning(f"Symbol {price['symbol']} has not enough data")
                logger.critical(f"Closing prices: {price}")
                current_week = FirstStageAnalysisModel(
                    uuid_analysis=analysis_indentifier,
                    uuid_currency=symbol.uuid,
                    closing_price=None,
                    open_price=None,
                    last_week_closing_price=None,
                    today=None,
                )
                first_stage_models.append(current_week)
                continue

            current_week = FirstStageAnalysisModel(
                uuid_analysis=analysis_indentifier,
                uuid_currency=symbol.uuid,
                closing_price=price["data"][6][4],
                open_price=price["data"][6][1],
                last_week_closing_price=price["data"][0][4],
                today=datetime.fromtimestamp(price["data"][6][6] / 1000),  # Convert milliseconds to seconds
            )
            first_stage_models.append(current_week)

        self.repository.save_all(self.session, first_stage_models)

    @show_runtime
    def collect(self, analysis_indentifier: Uuid):
        logger.info(f"Starting collecting open, close prices at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        prices = self._collect_binance_closing_prices()
        self.extract(analysis_indentifier, prices)

    def get_all_prices(self):
        start_time = datetime.now()

        prices = self.repository.get_all(self.session)
        prices_responses = [
            PricesResponse(
                symbol=self.symbols_repository.get_currency_info_by_uuid(self.session, price.uuid_currency).symbol,
                closing_price=price.closing_price,
                open_price=price.open_price,
                week=price.today,
            )
            for price in prices
        ]

        logger.info(f"Getting open, close prices from DB took {datetime.now() - start_time}h")
        return prices_responses

    @show_runtime
    def get_all_by_analysis_uuid(self, uuid: UUID, limit: int, offset: int):
        analysis, paginated = self.repository.get_paginated_by_uuid(self.session, uuid, limit, offset)  # type: ignore
        responses = []

        for anylise in analysis:
            response = FirstStageAnalysisResponse(
                currency=self._get_currency_entity(anylise.uuid_currency),  # type: ignore
                week_increase_percentage=(
                    float(anylise.week_increase_percentage) if anylise.week_increase_percentage else None
                ),
                valorization_date=anylise.today if anylise.today else None,  # type: ignore
                closing_price=float(anylise.closing_price) if anylise.closing_price else None,
                open_price=float(anylise.open_price) if anylise.open_price else None,
                last_week_closing_price=(
                    float(anylise.last_week_closing_price) if anylise.last_week_closing_price else None
                ),
                ema8=float(anylise.ema8) if anylise.ema8 else None,
                ema8_greater_open=bool(anylise.ema8_greater_open),
                ema8_less_close=bool(anylise.ema8_less_close),
            )

            responses.append(response)

        return responses, paginated

    def _get_currency_entity(self, symbol_uuid: UUID) -> AnalysisCurrencyInfo:
        currency = self.symbols_repository.get_currency_info_by_uuid(self.session, symbol_uuid)  # type: ignore
        return AnalysisCurrencyInfo(
            symbol=currency.symbol,  # type: ignore
            logo=currency.logo,  # type: ignore
            uuid=currency.uuid,  # type: ignore
            main_sector=self._get_sector_by_symbol(symbol_uuid),  # type: ignore
        )

    def _get_sector_by_symbol(self, symbol_uuid: UUID) -> SectorRead:
        try:
            model = self.sectors_service.get_by_symbol_uuid(self.session, symbol_uuid)[0]  # type: ignore
            return SectorRead(
                uuid=model.uuid,  # type: ignore
                title=model.title,  # type: ignore
            )
        except Exception as e:
            # logger.error(f"Error on [{symbol_uuid}]:\n{e}")
            return SectorRead(uuid=UUID("00000000-0000-0000-0000-000000000000"), title="Unknown")

    def get_price_by_symbol(self, symbol_str: str, analysis_uuid) -> FirstStageAnalysisModel:
        symbol = self.symbols_repository.get_currency_info_by_symbol(self.session, symbol_str)
        if symbol is None:
            raise HTTPException(status_code=404, detail="Criptomoeda não encontrada")

        first_stage = self.repository.get_by_symbol(self.session, symbol, analysis_uuid)

        if first_stage is None:
            raise HTTPException(status_code=404, detail="Análise não encontrada")

        return first_stage
