from loguru import logger
from sqlalchemy.orm import Session

from src.services.currencies_logo_collector import CurrenciesLogoCollector


def update_currencies_info(db: Session):
    logger.info("Updating currencies info")
    if db is not None:
        func_session: Session = db
        CurrenciesLogoCollector(session=func_session).collect_symbols_info()
    else:
        logger.critical("Database session is not available")
