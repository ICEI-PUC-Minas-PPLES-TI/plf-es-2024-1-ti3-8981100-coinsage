from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.currency_info import CurrencyInfoResponse
from src.services.analysis.first_stage.closing_price_service import PriceService
from src.services.currencies_info_collector import CurrenciesLogoCollector

router = APIRouter(
    prefix="/currency",
    tags=["Informações de Criptomoedas"],
)


@router.get(
    path="/",
    name="Informações bases das criptomoedas",
    response_model=CurrencyInfoResponse,
    description="Coletar logotipo, nome, descrição, documento técnico, URLs, etc. de todas as criptomoedas",
    responses={
        status.HTTP_200_OK: {"description": "Informações sobre criptomoedas recuperadas com sucesso."},
        status.HTTP_404_NOT_FOUND: {"description": "Nenhuma criptomoeda encontrada no banco de dados."},
    },
)
async def read_cryptos(db: Session = Depends(get_db)) -> CurrencyInfoResponse:
    cryptos = CurrenciesLogoCollector(session=db).get_cryptos()
    if len(cryptos.last_update.data) == 0:
        logger.warning("Nenhuma criptomoeda encontrada, iniciando coleta")
        CurrenciesLogoCollector(session=db).collect_symbols_info()
        cryptos = CurrenciesLogoCollector(session=db).get_cryptos()
    return cryptos
