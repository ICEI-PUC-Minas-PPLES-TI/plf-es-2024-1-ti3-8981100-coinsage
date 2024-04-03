import datetime

from src.config.manager import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import Session

from src.services.analysis_collector import AnalysisCollector
from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel

scheduler = AsyncIOScheduler()

db = None

@scheduler.scheduled_job(
    "cron",
    hour=settings.SCHEDULES["update_currencies_info"]["hour"],
    minute=settings.SCHEDULES["update_currencies_info"]["minute"],
    second=settings.SCHEDULES["update_currencies_info"]["second"],
    id="update_analysis_info",
)

def update_analysis_info():
    print("Puxe tudo aqui")
    logger.info("Updating analysis info")
    if db is not None:
        func_session: Session = db
        #! analysis_currency_stage_one | analysis_currency_stage_two | analysis_currency_stage_three | analysis_currency_stage_four    --> Utilizando a currency_base_info        
        AnalysisCollector(session=func_session).collect_symbols_info()
    else:
        logger.critical("Database session is not available")
        
              
def check_update_analysis_info(db: Session, settings: dict) -> None:
    next_update_time = (
        db.query(AnalysisInfoScheduleModel).order_by(AnalysisInfoScheduleModel.next_scheduled_time.desc()).first()
    )
    now: datetime = datetime.now()
    settings_time: datetime = now.replace(hour=settings["hour"], minute=settings["minute"], second=settings["second"])

    if next_update_time is not None:
        if next_update_time.last_update_time.date() == now.date():
            logger.info("Currencies info already updated today")
            return

        logger.info("Schedule is late. Updating now")
        update_analysis_info(db=db)
        return

    if settings_time < now:
        logger.info("Schedule never ran. Updating now")
        update_analysis_info(db=db)