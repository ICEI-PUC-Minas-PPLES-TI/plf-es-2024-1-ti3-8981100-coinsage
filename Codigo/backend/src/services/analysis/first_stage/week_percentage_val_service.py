from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from typing import Annotated

from fastapi import Depends
from loguru import logger
from sqlalchemy.orm import Session

from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.repository.crud import first_stage_repository
from src.services.analysis.first_stage.closing_price_service import ClosingPriceService
from src.utilities.runtime import show_runtime


class WeekPercentageValorizationService:
    def __init__(
        self, session: Session, closing_price_service: Annotated[ClosingPriceService, Depends(ClosingPriceService)]
    ):
        self.session = session
        self.closing_price_service = closing_price_service
        self.repository = first_stage_repository

    def _calculate_week_percentage_valorization(self, symbol: str, analysis_uuid) -> float:
        closes: FirstStageAnalysisModel = self.closing_price_service.get_closing_price_by_symbol(symbol, analysis_uuid)

        try:
            percentage_diff = (
                (closes.closing_price - closes.last_week_closing_price) / closes.last_week_closing_price * 100
            )
            logger.debug(
                f"Symbol: {symbol}, Current Week: {closes.closing_price}, Last Week: {closes.last_week_closing_price}"
            )
            logger.debug(f"Percentage Diff: {percentage_diff}")
            return float(percentage_diff)
        except TypeError as e:
            logger.error(f"Error on [{symbol}]:\n{e}")
            return 0.0

    @show_runtime
    def calculate_all_week_percentage_valorization(
        self, symbols: list[str], analysis_uuid
    ) -> list[FirstStageAnalysisModel]:
        all_diffs = []

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._calculate_week_percentage_valorization, symbol, analysis_uuid)
                for symbol in symbols
            ]

            for future, symbol in zip(futures, symbols):
                collected = future.result()
                all_diffs.append({symbol: collected})

        # update first stage model with week percentage valorization
        self.update_last(all_diffs, analysis_uuid)

        return self.repository.get_all(self.session)

    @show_runtime
    def update_last(self, increases, analysis_uuid):
        for increase in increases:
            symbol = list(increase.keys())[0]
            week_percentage = increase[symbol]
            self.repository.update_last_week_percentage(self.session, symbol, week_percentage, analysis_uuid)
