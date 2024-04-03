from datetime import datetime
from typing import Any, List
from uuid import UUID

from src.models.schemas.analysis.first_stage_analysis import FirstStageAnalysisResponse
from src.models.schemas.base import BaseSchemaModel


class AnalysisInfo(BaseSchemaModel):
    firstStageAnalysis: List[FirstStageAnalysisResponse] | Any


class LastUpdate(BaseSchemaModel):
    time: datetime
    data: AnalysisInfo


class AnalysisInfoResponse(BaseSchemaModel):
    next_update: datetime
    last_update: LastUpdate
