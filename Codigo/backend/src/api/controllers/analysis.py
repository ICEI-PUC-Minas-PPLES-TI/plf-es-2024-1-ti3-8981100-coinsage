from typing import List

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.analysis.analysis_info import AnalysisInfoResponse
from src.services.analysis.analysis_collector import AnalysisCollector
from src.services.currencies_info_collector import CurrenciesLogoCollector
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


@router.post(
    path="/start",
    name="Start Analysis",
    description="Iniciar a análise de dados.",
    status_code=status.HTTP_200_OK,
)
async def start_analysis(db: Session = Depends(get_db)):
    return AnalysisCollector(session=db).manually_start_analysis()


@router.post(
    path="/symbols/collect",
    name="Collect Symbols",
    description="Coletar símbolos de ações.",
    status_code=status.HTTP_200_OK,
)
async def collect_symbols(db: Session = Depends(get_db)):
    return CurrenciesLogoCollector(session=db).manually_collect_symbols()


@router.post(
    path="/sectors/collect",
    name="Collect Sectors",
    description="Coletar setores.",
    status_code=status.HTTP_200_OK,
)
async def collect_sectors(db: Session = Depends(get_db)):
    return SectorsCollector().manually_collect_sectors(db)
