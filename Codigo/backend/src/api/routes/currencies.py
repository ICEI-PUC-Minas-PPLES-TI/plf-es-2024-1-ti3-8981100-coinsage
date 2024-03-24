from uuid import UUID
import fastapi
from sqlalchemy.orm import Session
from loguru import logger

from src.api.dependencies.session import get_db
from src.models.schemas.currency_info import CurrencyInfo
from src.services.currencies_logo_collector import CurrenciesLogoCollector

router = fastapi.APIRouter(prefix="/currency", tags=["currency"])

@router.get(
    path="/all",
    name="users:get-all-crypto",
    response_model=list[CurrencyInfo],
    status_code=fastapi.status.HTTP_200_OK,
)
async def read_cryptos(db: Session = fastapi.Depends(get_db)) -> list[CurrencyInfo]:
    cryptos = CurrenciesLogoCollector(session=db).get_cryptos()
    if(len(cryptos) == 0):
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

# @router.get(
#     path="/{crypto_uuid}",
#     name="users:get-crypto",
#     response_model=CurrencyInfo,
#     status_code=fastapi.status.HTTP_200_OK,
# )
# async def read_crypto(crypto_uuid: str, db: Session = fastapi.Depends(get_db)) -> CurrencyInfo:
#     crypto = CurrenciesLogoCollector(session=db).get_crypto()
#     if crypto is None:
#         raise fastapi.HTTPException(status_code=404, detail="Crypto not found")
#     return crypto