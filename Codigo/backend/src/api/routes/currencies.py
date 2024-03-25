from uuid import UUID

import fastapi
from loguru import logger
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.currency_info import CurrencyInfo, CurrencyInfoResponse
from src.services.currencies_logo_collector import CurrenciesLogoCollector

router = fastapi.APIRouter(prefix="/currency", tags=["currency"])


@router.get(
    path="/all",
    name="users:get-all-crypto",
    response_model=CurrencyInfoResponse,
)
async def read_cryptos(db: Session = fastapi.Depends(get_db)) -> CurrencyInfoResponse:
    cryptos = CurrenciesLogoCollector(session=db).get_cryptos()
    if len(cryptos.last_update.data) == 0:
        logger.warning("No cryptos found, starting collect")
        CurrenciesLogoCollector(session=db).collect_symbols_info()
        cryptos = CurrenciesLogoCollector(session=db).get_cryptos()
    return cryptos


@router.post(
    path="/collect",
    name="users:collect-crypto",
    response_model=None,
    status_code=fastapi.status.HTTP_200_OK,
)
async def collect_cryptos(db: Session = fastapi.Depends(get_db)) -> None:
    CurrenciesLogoCollector(session=db).collect_symbols_info()