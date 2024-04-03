from datetime import datetime
from typing import List
from uuid import UUID

from src.models.schemas.base import BaseSchemaModel


class AnalysisInfo(BaseSchemaModel):
    symbol: str
    cmc_id: int
    cmc_slug: str
    urls: list[str]
    technical_doc: list[str]
    logo: str
    name: str
    description: str


class LastUpdate(BaseSchemaModel):
    time: datetime
    data: List[AnalysisInfo]


class AnalysisInfoResponse(BaseSchemaModel):
    next_update: datetime
    last_update: LastUpdate