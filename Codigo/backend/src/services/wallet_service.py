from datetime import datetime
from decimal import Decimal
from typing import Any, List
from uuid import UUID

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm import Session

from src.models import schemas
from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.wallet_transaction import WalletTransaction
from src.models.schemas.currency_info import SimpleCrypto
from src.models.schemas.timestamp_price import TimestampPrice
from src.models.schemas.user import UserResponse
from src.models.schemas.wallet import ProfitCompare
from src.repository.crud import currency_info_repository, wallet_repository
from src.services.price_timestamp_service import PriceAtTimestampService


class WalletService:
    def __init__(self):
        self.repository = wallet_repository
        self.cryptos_repository = currency_info_repository
        self.price_service = PriceAtTimestampService()

    def create_buy(self, create: schemas.BuyWalletCreate, user: UserResponse, db: Session = None):
        user_id = user.id
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")
        crypto = self.cryptos_repository.get_currency_info_by_symbol(db=db, symbol=create.crypto)
        if not crypto:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")

        created_model = self.repository.create_buy(db=db, buy=create, currency_uuid=crypto.uuid, user_id=user_id)
        return schemas.CompleteWalletTransaction(
            # format dd/mm/yyyy/ h:m
            date=created_model.date.strftime("%d-%m-%Y %H:%M"),
            crypto=create.crypto,
            quantity=created_model.quantity,
            amount=created_model.amount,
            price_on_purchase=created_model.price_on_purchase,
            created_at=created_model.created_at,
            uuid=created_model.uuid,
            user_id=created_model.user_id,
        )

    def profit(self, db: Session, transaction_uuid: UUID, user: UserResponse) -> schemas.ResponseProfitCompare:
        user_id = user.id
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")

        transaction = self.repository.get_by_uuid(db, transaction_uuid, user_id)

        if transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")

        coin = self.cryptos_repository.get_currency_info_by_uuid(db, transaction.uuid_currency)
        if coin is None:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")

        profit = self._calculate_profit(transaction, coin, db)

        return profit

    def _calculate_profit(
        self, transaction: WalletTransaction, coin: CurrencyBaseInfoModel, db: Session = None
    ) -> schemas.ResponseProfitCompare:
        packet = TimestampPrice(crypto=coin.symbol, date=datetime.now().strftime("%d-%m-%Y %H:%M"))
        current_price = self.price_service.get_price_by_date_time(packet=packet, session=db)
        profit_percentage = self._profit_percentage(Decimal(current_price), transaction.price_on_purchase)

        return schemas.ResponseProfitCompare(
            crypto=SimpleCrypto(symbol=coin.symbol, name=coin.name, logo=coin.logo, uuid=coin.uuid),
            transaction_uuid=transaction.uuid,
            profit=ProfitCompare(
                buy_date=transaction.date,
                buy_price=transaction.price_on_purchase,
                compare_date=datetime.now(),
                current_price=Decimal(current_price),
                buy_value=Decimal(
                    transaction.amount
                    if transaction.amount is not None
                    else transaction.price_on_purchase * transaction.quantity
                ),
                current_value=self._calculate_current_value(
                    buy_value=Decimal(
                        transaction.amount
                        if transaction.amount is not None
                        else transaction.price_on_purchase * transaction.quantity
                    ),
                    current_price=Decimal(current_price),
                    buy_price=transaction.price_on_purchase,
                ),
                profit=profit_percentage,
            ),
        )

    def _profit_percentage(self, current_value: Decimal, buy_value: Decimal) -> Decimal:
        if not buy_value:
            return Decimal(0)
        return Decimal(round(((current_value - buy_value) / buy_value) * 100, 2))

    def _calculate_current_value(self, buy_value: Decimal, current_price: Decimal, buy_price: Decimal) -> Decimal:
        if not buy_price:
            return Decimal(0)
        return Decimal((current_price * buy_value) / buy_price)

    def list_transactions_by_user(self, db: Session, user: UserResponse, limit: int, offset: int, sort: List[str]):
        user_id = user.id
        transactions, paginated = self.repository.list_all_transactions_by_user(db, user_id, limit, offset, sort)
        responses: List[schemas.ResponseProfitCompare] = []

        if len(transactions) > 0:
            for transaction in transactions:
                response = self._calculate_profit(transaction[0], transaction[1], db)
                responses.append(response)

        try:
            return schemas.WalletListResponse(
                data=responses,
                page=paginated.page,
                total=paginated.total,
                remaining=paginated.remaining,
            )
        except Exception as err:
            logger.error(f"Error on list_transactions_by_user: {err}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error on listing transactions"
            )
