from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.analysis.analysis_info import AnalysisInfoResponse
from src.services.analysis.analysis_collector import AnalysisCollector
from src.services.sectors_info_collector import SectorsCollector

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get(
    path="/first_stage",
    name="First Stage Analysis",
    response_model=AnalysisInfoResponse,
    description="Coletar dados da primeira etapa da última análise realizada pelo sistema.",
    status_code=status.HTTP_200_OK,
)
async def get_last_first_stage_analysis(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=0),
    offset: int = Query(0, ge=0),
    sort: List[str] = Query([]),
) -> AnalysisInfoResponse:
    return AnalysisCollector(session=db).get_last_first_stage_analysis(limit, offset, sort)
