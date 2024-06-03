from fastapi import APIRouter, Depends, status
from loguru import logger
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models import schemas
from src.models.schemas.user import UserCreate
from src.security.authentication import get_current_user
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
async def read_cryptos(
    new_transaction: schemas.BuyWalletCreate,
    db: Session = Depends(get_db),
    current_user: UserCreate = Depends(get_current_user),
):
    return service.create_buy(new_transaction, current_user, db)
