import time
from typing import Any

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from src.models.db.currencies_info_schedule import CurrenciesInfoScheduleModel
from src.repository.crud import currencies_info_schedule_repository


class CurrenciesInfoScheduleService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = currencies_info_schedule_repository

    def get_last_update(self) -> CurrenciesInfoScheduleModel:
        last_update = self.repository.get_last_update(self.session)
        if last_update is None:
            logger.error(f"Error on get last update on currencies info from database")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Last update not found!")

        return last_update
