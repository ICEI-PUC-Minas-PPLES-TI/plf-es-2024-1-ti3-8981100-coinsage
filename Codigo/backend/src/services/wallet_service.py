from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.models import schemas
from src.repository.crud import currency_info_repository, wallet_repository


class WalletService:
    def __init__(self):
        self.repository = wallet_repository
        self.cryptos_repository = currency_info_repository

    def create_buy(self, create: schemas.BuyWalletCreate, db: Session = None):
        crypto = self.cryptos_repository.get_currency_info_by_symbol(db=db, symbol=create.crypto)
        if not crypto:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")

        created_model = self.repository.create_buy(db=db, buy=create, currency_uuid=crypto.uuid)
        return schemas.CompleteWalletTransaction(
            date=created_model.date.strftime("%d-%m-%Y %H:%M"),
            crypto=create.crypto,
            quantity=created_model.quantity,
            amount=created_model.amount,
            price_on_purchase=created_model.price_on_purchase,
            created_at=created_model.created_at,
            uuid=created_model.uuid,
        )
