from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models import schemas
from src.models.schemas.currency_info import CurrencyInfoResponse
from src.services.analysis.first_stage.closing_price_service import PriceService
from src.services.currencies_info_collector import CurrenciesLogoCollector
from src.services.price_timestamp_service import PriceAtTimestampService

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


# get price by date and time
@router.get(
    path="/price/{crypto}/{date}",
    name="Preço de uma criptomoeda em um momento específico",
    description="Coletar o preço de uma criptomoeda em um momento específico",
    responses={
        status.HTTP_200_OK: {"description": "Preço da criptomoeda recuperado com sucesso."},
        status.HTTP_404_NOT_FOUND: {"description": "Criptomoeda não encontrada."},
    },
)
async def get_price_by_date_time(date: str, crypto: str, db: Session = Depends(get_db)):
    packet = schemas.TimestampPrice(crypto=crypto, date=date)
    return PriceAtTimestampService().get_price_by_date_time(packet, session=db)


@router.get(
    path="/query/{match}",
    name="Consultar criptomoeda por nome ou símbolo",
    description="Consultar informações de uma criptomoeda por nome ou símbolo",
    responses={
        status.HTTP_200_OK: {"description": "Informações da criptomoeda recuperadas com sucesso."},
        status.HTTP_404_NOT_FOUND: {"description": "Criptomoeda não encontrada."},
    },
)
async def query_crypto(match: str, db: Session = Depends(get_db)):
    return CurrenciesLogoCollector(session=db).get_crypto_by_name_or_symbol(match)


@router.get(
    path="/query",
    name="Consultar criptomoeda por nome ou símbolo",
    description="Consultar informações de uma criptomoeda por nome ou símbolo",
    responses={
        status.HTTP_200_OK: {"description": "Informações da criptomoeda recuperadas com sucesso."},
        status.HTTP_404_NOT_FOUND: {"description": "Criptomoeda não encontrada."},
    },
)
async def query_all(db: Session = Depends(get_db)):
    return CurrenciesLogoCollector(session=db).get_all_reduced()
