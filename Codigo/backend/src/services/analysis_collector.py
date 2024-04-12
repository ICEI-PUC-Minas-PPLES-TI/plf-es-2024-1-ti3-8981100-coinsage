import datetime
import time
from typing import Any, List

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.analysis import Analysis
from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel
from src.models.schemas.analysis.analysis_info import AnalysisInfo, AnalysisInfoResponse, LastUpdate
from src.models.schemas.analysis.first_stage_analysis import FirstStageAnalysisResponse
from src.models.schemas.currency_info import CurrencyInfo, CurrencyInfoResponse
from src.repository.crud import analysis_info_repository, analysis_info_schedule_repository
from src.services.analysis.first_stage.closing_price_service import ClosingPriceService
from src.services.analysis.first_stage.week_percentage_val_service import WeekPercentageValorizationService
from src.services.currencies_info_collector import CurrenciesLogoCollector
from src.utilities.runtime import show_runtime


class AnalysisCollector:
    def __init__(self, session: Session):
        self.session = session
        self.symbols_service: CurrenciesLogoCollector = CurrenciesLogoCollector(session=session)
        self.repository = analysis_info_repository
        self.schedule_repository = analysis_info_schedule_repository

        # flows
        self.closing_price_service = ClosingPriceService(session=session)
        self.week_increse_service = WeekPercentageValorizationService(
            session=session, closing_price_service=self.closing_price_service
        )

    def _clear_table(self):
        self.repository.clear_table(self.session)

    def _new_analysis(self) -> Analysis:
        analysis: Analysis = Analysis()
        self.session.add(analysis)
        self.session.commit()
        self.session.refresh(analysis)
        return analysis

    @show_runtime
    def start_analysis(self):
        new_analysis: Analysis = self._new_analysis()

        cryptos_str: List[str] = [crypto.symbol for crypto in self.symbols_service.get_cryptos().last_update.data]
        self.closing_price_service.collect(analysis_indentifier=new_analysis.uuid)
        self.week_increse_service.calculate_all_week_percentage_valorization(cryptos_str, new_analysis.uuid)

        self.session.add(AnalysisInfoScheduleModel(next_scheduled_time=self.calculate_next_time()))
        self.session.commit()

    def calculate_next_time(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(days=1)

    def get_last_analysis(self):
        last_analysis: Analysis | None = self.repository.get_last(self.session)
        schedule: AnalysisInfoScheduleModel | None = self.schedule_repository.get_last_update(self.session)

        if last_analysis and schedule:
            all_first_stage: List[FirstStageAnalysisResponse] = self.closing_price_service.get_all_by_analysis_uuid(
                last_analysis.uuid
            )

            try:
                analysis = AnalysisInfo(firstStageAnalysis=all_first_stage)
                return AnalysisInfoResponse(
                    next_update=schedule.next_scheduled_time,  # type: ignore
                    last_update=LastUpdate(time=last_analysis.date, data=analysis),  # type: ignore
                )
            except Exception as e:
                logger.error(f"Error on get_last_analysis: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on get_last_analysis"
                )

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No analysis found")
