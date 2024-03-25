from datetime import datetime
from typing import List
from pydantic import BaseModel, validator

from src.utilities.formatters.datetime_formatter import format_datetime


class CurrencyInfo(BaseModel):
    symbol: str
    cmc_id: int
    cmc_slug: str
    logo: str
    name: str
    description: str
    technical_doc: list[str]
    urls: list[str]

    class Config:
        from_attributes = True

class LastUpdate(BaseModel):
    time: str
    data: List[CurrencyInfo]
    
    @validator("time", pre=True)
    def format_time(cls, value: datetime) -> str:
        return format_datetime(value)
    
    class Config:
        from_attributes = True
class CurrencyInfoResponse(BaseModel):
    next_update: str
    last_update: LastUpdate
    
    @validator("next_update", pre=True)
    def format_time(cls, value: datetime) -> str:
        return format_datetime(value)
    
    class Config:
        from_attributes = True
