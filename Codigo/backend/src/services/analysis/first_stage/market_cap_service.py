import datetime
from typing import Any, List
from uuid import UUID

from loguru import logger
from sqlalchemy.orm import Session

from src.models import Analysis
from src.repository.crud import first_stage_repository
from src.services.externals import CMCMarketCapCollector
from src.utilities.runtime import show_runtime


class MarketCapService:
    def __init__(self):
        self.collector = CMCMarketCapCollector()
        self.first_stage_repository = first_stage_repository
        self.chunk_size = 150

    @show_runtime
    def collect(self, db: Session, analysis: Analysis, cryptos_str: List[str]) -> None:
        logger.info(
            f"Starting market cap collection for {len(cryptos_str)} symbols at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        results = self.collector.collect(cryptos_str)
        for result in results:
            self._save_market_cap(db, analysis.uuid, result)

    def _save_market_cap(self, db: Session, analysis_uuid: UUID, cap: Any) -> None:
        corresponding = self.first_stage_repository.get_by_symbol_str(db, cap["symbol"], analysis_uuid)

        if corresponding is None:
            logger.error(f"FirstStageAnalysisModel not found for [{analysis_uuid}]")
            return

        market_cap = round(cap["quote"]["USD"]["market_cap"], 8)

        corresponding.market_cap = market_cap
        db.commit()
