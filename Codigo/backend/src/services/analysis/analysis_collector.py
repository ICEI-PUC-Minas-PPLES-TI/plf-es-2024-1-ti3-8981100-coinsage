import datetime
import threading
from typing import List

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.analysis import Analysis
from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel
from src.models.schemas.analysis.analysis_info import AnalysisInfo, AnalysisInfoResponse, LastUpdate
from src.repository.crud import analysis_info_repository, analysis_info_schedule_repository, first_stage_repository
from src.services.analysis.first_stage.closing_price_service import PriceService
from src.services.analysis.first_stage.daily_volume_service import DailyVolumeService
from src.services.analysis.first_stage.ema_calculator_service import EmaCalculatorService
from src.services.analysis.first_stage.market_cap_service import MarketCapService
from src.services.analysis.first_stage.week_percentage_val_service import WeekPercentageValorizationService
from src.services.analysis.second_stage.variation_per_service import VariationPer
from src.services.currencies_info_collector import CurrenciesLogoCollector
from src.utilities.runtime import show_runtime


class AnalysisCollector:
    def __init__(self, session: Session):
        self.session = session
        self.session.expire_on_commit = False
        self.symbols_service: CurrenciesLogoCollector = CurrenciesLogoCollector(session=session)
        self.repository = analysis_info_repository
        self.schedule_repository = analysis_info_schedule_repository
        self.first_stage_repo = first_stage_repository

        # flows
        self.prices_service = PriceService(session=session)
        self.week_increse_service = WeekPercentageValorizationService(
            session=session, closing_price_service=self.prices_service
        )
        self.ema_calculator_service = EmaCalculatorService()
        self.market_cap_service = MarketCapService()
        self.volume_service = DailyVolumeService(session=session)
        self.variation_per_service = VariationPer(session=session)

    def _new_analysis(self) -> Analysis:
        analysis: Analysis = Analysis()
        self.session.add(analysis)
        self.session.commit()
        self.session.refresh(analysis)
        return analysis

    def _finish_analysis(self, analysis: Analysis):
        self.repository.update_ended(self.session, analysis.uuid)  # type: ignore

    def _delete_analysis_related(self, analysis: Analysis):
        item = (
            self.session.query(AnalysisInfoScheduleModel)
            .where(AnalysisInfoScheduleModel.uuid_analysis == analysis.uuid)
            .first()
        )
        if item is not None:
            self.session.delete(item)
            self.session.commit()

        self.first_stage_repo.delete_not_ended(self.session, analysis.uuid)  # type: ignore
        self.repository.delete(self.session, analysis.uuid)  # type: ignore

    @show_runtime
    def start_analysis(self):
        logger.info(f"Starting analysis at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        new_analysis: Analysis = self._new_analysis()
        try:
            symbols = self.symbols_service.get_cryptos().last_update.data
            cryptos_str: List[str] = [crypto.symbol for crypto in symbols]

            thread1 = threading.Thread(target=self.prices_service.collect_current_price, args=(new_analysis.uuid,))
            thread2 = threading.Thread(target=self.volume_service.fetch_volume_data, args=(new_analysis.uuid,))
            thread3 = threading.Thread(
                target=self.variation_per_service.fetch_variation_price, args=(new_analysis.uuid,)
            )

            self.prices_service.collect(analysis_indentifier=new_analysis.uuid)
            self.market_cap_service.collect(db=self.session, analysis=new_analysis, cryptos_str=cryptos_str)
            self.week_increse_service.calculate_all_week_percentage_valorization(cryptos_str, new_analysis.uuid)
            self.ema_calculator_service.append_ema8_and_relations(self.session, symbols, new_analysis.uuid)
            self.ema_calculator_service.calculate_crossovers(self.session, symbols, new_analysis.uuid)

            thread1.start()
            thread2.start()
            thread3.start()

            thread1.join()
            thread2.join()
            thread3.join()

            self.session.add(
                AnalysisInfoScheduleModel(
                    next_scheduled_time=self.calculate_next_time(), uuid_analysis=new_analysis.uuid
                )
            )
            self.session.commit()

            self._finish_analysis(new_analysis)
        except Exception as err:
            logger.error(f"Error on start_analysis: {err}")
            self._delete_analysis_related(new_analysis)
            self.session.rollback()

    def calculate_next_time(self) -> datetime.datetime:
        return datetime.datetime.now() + datetime.timedelta(days=1)

    @show_runtime
    def get_last_first_stage_analysis(self, limit: int, offset: int):
        last_analysis: Analysis | None = self.repository.get_last(self.session)
        schedule: AnalysisInfoScheduleModel | None = self.schedule_repository.get_last_update(self.session)

        if last_analysis:
            all_first_stage, paginated = self.prices_service.get_all_by_analysis_uuid(
                last_analysis.uuid, limit, offset
            )

            try:
                analysis = AnalysisInfo(
                    data=all_first_stage, total=paginated.total, remaining=paginated.remaining, page=paginated.page
                )
                return AnalysisInfoResponse(
                    next_update=schedule.next_scheduled_time if schedule else None,  # type: ignore
                    last_update=LastUpdate(time=last_analysis.date, data=analysis),  # type: ignore
                )
            except Exception as e:
                logger.error(f"Error on get_last_analysis: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on getting last analysis"
                )

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No analysis found")
