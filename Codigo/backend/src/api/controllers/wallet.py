from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models import schemas
from src.services import WalletService

service = WalletService()

router = APIRouter(
    prefix="/wallet",
    tags=["Informações do seu portifólio"],
)


@router.post(
    path="/",
    name="Informações bases das criptomoedas",
    description="Criar uma nova transação de compra de criptomoedas",
    responses={
        status.HTTP_200_OK: {"description": "Transação de compra de criptomoeda criada com sucesso."},
    },
    response_model=schemas.CompleteWalletTransaction,
)
async def read_cryptos(create: schemas.BuyWalletCreate, db: Session = Depends(get_db)):
    return service.create_buy(create, db)
