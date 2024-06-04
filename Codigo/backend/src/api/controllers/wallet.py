from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models import schemas
from src.models.schemas.user import UserResponse
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
async def new_transaction(
    new_transaction: schemas.BuyWalletCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return service.create_buy(new_transaction, current_user, db)


@router.get(
    path="/profit",
    name="Lucro",
    description="Verificar o lucro de uma criptomoeda, compando seu valor de compra, e valor comprado com o valor atual da criptomoeda.",
    responses={
        status.HTTP_200_OK: {"description": "Lucro calculado com sucesso."},
    },
    response_model=schemas.ResponseProfitCompare,
)
async def calculate_profit(
    uuid: UUID, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)
) -> schemas.ResponseProfitCompare:
    return service.profit(db=db, transaction_uuid=uuid, user=current_user)
