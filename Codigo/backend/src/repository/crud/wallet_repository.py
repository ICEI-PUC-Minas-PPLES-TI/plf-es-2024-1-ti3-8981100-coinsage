from typing import List

from loguru import logger
from sqlalchemy import BigInteger, func, select, Uuid
from sqlalchemy.orm import Session

from src.models import schemas
from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.wallet_transaction import WalletTransaction
from src.models.schemas.generic_pagination import PaginatedResponse


def create_buy(
    db: Session, buy: schemas.BuyWalletCreate, currency_uuid: Uuid, user_id: BigInteger
) -> WalletTransaction:
    db_transaction = WalletTransaction(
        quantity=buy.quantity,
        amount=buy.amount,
        date=buy._date,
        price_on_purchase=buy.price_on_purchase,
        uuid_currency=currency_uuid,
        user_id=user_id,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_by_uuid(db: Session, transaction_uuid: Uuid, user_id: BigInteger) -> WalletTransaction:
    return (
        db.query(WalletTransaction)
        .filter(WalletTransaction.uuid == transaction_uuid, WalletTransaction.user_id == user_id)
        .first()
    )


def list_all_transactions_by_user(
    db: Session, user_id: BigInteger, limit: int, offset: int, sort: List[str]
) -> list[WalletTransaction]:
    query = (
        db.query(WalletTransaction, CurrencyBaseInfoModel)
        .join(CurrencyBaseInfoModel, WalletTransaction.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(WalletTransaction.user_id == user_id)
    )
    if len(sort) > 0:
        column, direction = sort[0].split(",")
        column_attr = None
        try:
            column_attr = getattr(WalletTransaction, column)
        except AttributeError:
            logger.error(f"Column {column} not found in WalletTransaction")
        if column_attr:
            if direction == "asc":
                query = query.order_by(column_attr.asc().nulls_last())
            else:
                query = query.order_by(column_attr.desc().nulls_last())
    else:
        query = query.order_by(WalletTransaction.date.desc())

    queried = query.limit(limit).offset(offset).all()
    count = db.scalar(select(func.count()).where(WalletTransaction.user_id == user_id))
    remaining = max(count - (limit + offset), 0)  # type: ignore

    return list(queried), PaginatedResponse(total=count, remaining=remaining, page=limit if count > limit else count)  # type: ignore
