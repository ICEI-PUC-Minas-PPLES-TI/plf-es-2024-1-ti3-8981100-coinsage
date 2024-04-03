from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import Session

from src.config.manager import settings

# App schedules
from .update_currencies_info import check_update_currencies_info, update_currencies_info
from .update_analysis_info import check_update_analysis_info, update_analysis_info

scheduler = AsyncIOScheduler()

db = None


def start_schedules(app_db: Session):
    global db
    db = app_db
    logger.info("Checking all schedules")
    check_all_schedules()

    scheduler.start()
    logger.info("Schedules started")


def stop_schedules():
    scheduler.shutdown()
    logger.info("Schedules stopped")


def check_all_schedules():
    if db is None:
        logger.critical("Database session is not available")
        return

    check_update_currencies_info(db=db, settings=settings.SCHEDULES["update_currencies_info"])
    check_update_analysis_info(db=db, settings=settings.SCHEDULES["update_analysis_info"])


# =======  All app schedules =======
@scheduler.scheduled_job(
    "cron",
    hour=settings.SCHEDULES["update_currencies_info"]["hour"],
    minute=settings.SCHEDULES["update_currencies_info"]["minute"],
    second=settings.SCHEDULES["update_currencies_info"]["second"],
    id="update_currencies_info",
)
def schedule_update_currencies_info():
    if db is None:
        logger.critical("Database session is not available")
        return
    update_currencies_info(db=db)