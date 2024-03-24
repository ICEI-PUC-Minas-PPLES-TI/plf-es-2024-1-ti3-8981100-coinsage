from sqlalchemy.orm import Session
from src.services.currencies_logo_collector import CurrenciesLogoCollector
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.config.manager import settings

scheduler = AsyncIOScheduler()

db = None
def start_schedules(app_db: Session):
    global db
    db = app_db
    scheduler.start()
    logger.info("Schedules started")

@scheduler.scheduled_job("cron", 
                         hour=settings.SCHEDULES["update_currencies_info"]["hour"], 
                         minute=settings.SCHEDULES["update_currencies_info"]["minute"], 
                         second=settings.SCHEDULES["update_currencies_info"]["second"], 
                         id="update_currencies_info")
def update_currencies_info():
    logger.info("Updating currencies info")
    if db is not None:
        func_session: Session = db
        CurrenciesLogoCollector(session=func_session).collect_symbols_info()
    else:
        logger.critical("Database session is not available")