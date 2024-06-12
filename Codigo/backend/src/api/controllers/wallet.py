from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
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


@router.get(
    path="/",
    name="Lista de Transações",
    description="Listar todas as transações de compra passadas.",
    response_model=schemas.WalletListResponse,
    responses={status.HTTP_200_OK: {"description": "Transações listadas com sucesso."}},
)
async def list_transactions(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
    limit: int = Query(20, ge=0),
    offset: int = Query(0, ge=0),
    sort: List[str] = Query([]),
):
    response = service.list_transactions_by_user(db, current_user, limit, offset, sort)
    return response

@router.delete(
        "/{uuid}",
        name="Deletar Transação",
        description="Deletar uma transação específica.",
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Transação deletada com sucesso."},
            status.HTTP_404_NOT_FOUND: {"description": "Transação não encontrada."},
            status.HTTP_403_FORBIDDEN: {"description": "Ação não permitida."},
        }
)
async def delete_transaction(
    uuid: UUID,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
) -> None:
    success = service.delete_transaction_by_uuid(uuid, db, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Transação não encontrada para o usuário.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
