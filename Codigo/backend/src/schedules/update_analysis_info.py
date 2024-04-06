from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import Session

from src.config.manager import settings
from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel
from src.services.analysis.analysis_collector import AnalysisCollector

def update_analysis_info(db: Session) -> None:
    logger.info("Updating analysis info")
    AnalysisCollector(session=db).start_analysis()


def check_update_analysis_info(db: Session, settings: dict) -> None:
    next_update_time = (
        db.query(AnalysisInfoScheduleModel).order_by(AnalysisInfoScheduleModel.next_scheduled_time.desc()).first()
    )
    now: datetime = datetime.now()
    settings_time: datetime = now.replace(hour=settings["hour"], minute=settings["minute"], second=settings["second"])

    if next_update_time is not None:
        if next_update_time.last_update_time.date() == now.date():
            logger.info("Analysis info already updated today")
            return

        logger.info("Schedule is late. Updating now")
        update_analysis_info(db=db)
        return

    if settings_time < now:
        logger.info("Schedule never ran. Updating now")
        update_analysis_info(db=db)
