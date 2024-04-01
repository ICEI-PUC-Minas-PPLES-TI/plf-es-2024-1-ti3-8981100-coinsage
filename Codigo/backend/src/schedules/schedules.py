from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import Session

from src.config.manager import settings

# App schedules
from .update_currencies_info import update_currencies_info

scheduler = AsyncIOScheduler()

db = None


def start_schedules(app_db: Session):
    global db
    db = app_db
    scheduler.start()
    logger.info("Schedules started")


def stop_schedules():
    scheduler.shutdown()
    logger.info("Schedules stopped")


# =======  All app schedules =======
@scheduler.scheduled_job(
    "cron",
    hour=settings.SCHEDULES["update_currencies_info"]["hour"],
    minute=settings.SCHEDULES["update_currencies_info"]["minute"],
    second=settings.SCHEDULES["update_currencies_info"]["second"],
    id="update_currencies_info",
)
def schedule_update_currencies_info():
    if db is not None:
        update_currencies_info(db=db)
        return
    logger.critical("Database session is not available")
