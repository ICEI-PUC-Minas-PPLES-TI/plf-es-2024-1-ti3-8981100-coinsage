from datetime import datetime

from loguru import logger
from sqlalchemy.orm import Session

from src.models.db.currencies_info_schedule import CurrenciesInfoScheduleModel
from src.services.currencies_logo_collector import CurrenciesLogoCollector


def update_currencies_info(db: Session) -> None:
    logger.info("Updating currencies info")
    func_session: Session = db
    CurrenciesLogoCollector(session=func_session).collect_symbols_info()


def check_update_currencies_info(db: Session, settings: dict) -> None:
    next_update_time = (
        db.query(CurrenciesInfoScheduleModel).order_by(CurrenciesInfoScheduleModel.next_scheduled_time.desc()).first()
    )
    now: datetime = datetime.now()
    settings_time: datetime = now.replace(hour=settings["hour"], minute=settings["minute"], second=settings["second"])

    if next_update_time is not None:
        if next_update_time.last_update_time.date() == now.date():
            logger.info("Currencies info already updated today")
            return

        logger.info("Schedule is late. Updating now")
        update_currencies_info(db=db)
        return

    if settings_time < now:
        logger.info("Schedule never ran. Updating now")
        update_currencies_info(db=db)
