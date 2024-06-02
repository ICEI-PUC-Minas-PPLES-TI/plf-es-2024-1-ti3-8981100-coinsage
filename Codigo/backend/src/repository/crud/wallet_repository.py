from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models import schemas
from src.models.db.wallet_transaction import WalletTransaction


def create_buy(db: Session, buy: schemas.BuyWalletCreate, currency_uuid: Uuid) -> WalletTransaction:
    db_transaction = WalletTransaction(
        quantity=buy.quantity,
        amount=buy.amount,
        date=buy._date,
        price_on_purchase=buy.price_on_purchase,
        uuid_currency=currency_uuid,
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_by_uuid(db: Session, transaction_uuid: Uuid) -> WalletTransaction:
    return db.query(WalletTransaction).filter(WalletTransaction.uuid == transaction_uuid).first()
