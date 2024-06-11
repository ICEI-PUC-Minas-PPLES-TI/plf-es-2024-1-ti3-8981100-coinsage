from datetime import datetime

from loguru import logger
from sqlalchemy.orm import Session

from src.models.db.sector_info_schedule import SectorInfoScheduleModel
from src.services.sectors_info_collector import SectorsCollector


def update_sectors(db: Session) -> None:
    logger.info("Updating sectors")
    SectorsCollector().collect(db_session=db)


def check_update_sectors(db: Session, settings: dict) -> None:
    next_update_time = (
        db.query(SectorInfoScheduleModel).order_by(SectorInfoScheduleModel.next_scheduled_time.desc()).first()
    )
    now: datetime = datetime.now()
    settings_time: datetime = now.replace(hour=settings["hour"], minute=settings["minute"], second=settings["second"])

    if next_update_time is not None:
        if next_update_time.last_update_time.date() == now.date():
            logger.info("Sectors already updated today")
            return

        logger.info("Schedule is late. Updating now")
        update_sectors(db=db)
        return

    if settings_time < now:
        logger.info("Schedule never ran. Updating now")
        update_sectors(db=db)
