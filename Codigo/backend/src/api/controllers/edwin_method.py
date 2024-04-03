from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.analysis.analysis_info import AnalysisInfoResponse
from src.services.analysis_collector import AnalysisCollector

router = APIRouter(prefix="/edwin_method", tags=["edwin_method"])


@router.get(
    path="/",
    name="edwin_method:read-last-analysis",
    response_model=AnalysisInfoResponse,
    description="Coletar dados da última análise.",
    status_code=status.HTTP_200_OK,
)
async def get_accounts(db: Session = Depends(get_db)) -> AnalysisInfoResponse:
    analysis = AnalysisCollector(session=db).get_last_analysis()
    return analysis
