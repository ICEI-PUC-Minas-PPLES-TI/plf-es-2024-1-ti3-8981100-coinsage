from typing import List

from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models import Analysis
from src.repository.crud import first_stage_repository
from src.services.analysis.first_stage.market_cap_service import MarketCapService
from src.services.currencies_info_collector import CurrenciesLogoCollector
from src.utilities.runtime import show_runtime


class RankingService:
    """Collect CMC rankings"""
    def __init__(self, session: Session):
        self.session = session
        self.first_stage_repo = first_stage_repository
        self.symbols_service: CurrenciesLogoCollector = CurrenciesLogoCollector(session=session)
        self.market_cap_service = MarketCapService()
    

    @show_runtime
    def update_market_cap_rankings(self, session: Session, analysis: Analysis, cryptos_str: List[str]) -> None:
        try:
            market_caps = self.market_cap_service.collect_and_return(cryptos_str)
            sorted_market_caps = sorted(market_caps, key=lambda x: x["quote"]["USD"]["market_cap"], reverse=True)

            for index, cap in enumerate(sorted_market_caps):
                symbol = str(cap["symbol"])
                new_rank = index + 1
                analysis_uuid: Uuid = analysis.uuid
                self.first_stage_repo.update_ranking(session, symbol, new_rank, analysis_uuid)
            
            logger.info("Rankings updated.")
        except Exception as err:
            logger.error(f"Error while updating rankings: {err}")
