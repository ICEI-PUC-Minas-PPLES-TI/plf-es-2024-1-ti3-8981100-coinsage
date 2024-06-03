from datetime import datetime, timedelta
from decimal import Decimal
from unittest import mock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.user import UserModel
from src.models.db.wallet_transaction import WalletTransaction
from src.models.schemas.timestamp_price import TimestampPrice
from src.models.schemas.user import UserResponse
from src.services.wallet_service import WalletService
from tests.db.db_fixture import test_session


@pytest.fixture(scope="function")
def crypto_on_database(test_session):
    coin = CurrencyBaseInfoModel(
        symbol="BTC",
        cmc_id=1,
        cmc_slug="bitcoin",
        logo="https://bitcoin.com",
        name="Bitcoin",
        description="The first cryptocurrency",
        technical_doc=["https://bitcoin.com/technical"],
        urls=["https://bitcoin.com"],
    )
    test_session.add(coin)
    test_session.commit()
    test_session.refresh(coin)

    coin2 = CurrencyBaseInfoModel(
        symbol="ETH",
        cmc_id=2,
        cmc_slug="ethereum",
        logo="https://ethereum.com",
        name="Ethereum",
        description="The second cryptocurrency",
        technical_doc=["https://ethereum.com/technical"],
        urls=["https://ethereum.com"],
    )
    test_session.add(coin2)
    test_session.commit()
    test_session.refresh(coin2)

    user = UserModel(id=1, email="user@test.com", password="password", name="User")
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)

    return [coin, coin2, user]


@pytest.fixture(scope="function")
def transaction_on_database(test_session, crypto_on_database):
    def create_transaction(quantity, amount, price_on_purchase):
        transaction = WalletTransaction(
            uuid=uuid4(),
            date=datetime.now() - timedelta(days=1),
            quantity=quantity,
            amount=amount,
            price_on_purchase=price_on_purchase,
            created_at=datetime.now(),
            uuid_currency=crypto_on_database[0].uuid,
            user_id=crypto_on_database[2].id,
        )
        test_session.add(transaction)
        test_session.commit()
        test_session.refresh(transaction)
        return transaction

    return create_transaction


@pytest.mark.parametrize(
    "quantity, amount, price_on_purchase, current_price, expected_profit, expected_buy_value, expected_current_value",
    [
        (None, Decimal(60000.0), Decimal(20000.0), Decimal(75000.0), Decimal(275), Decimal(60000.0), Decimal(225000)),
        (1.5, None, Decimal(30000.0), Decimal(75000.0), Decimal(150), Decimal(45000.0), Decimal(112500)),
        (3.0, None, Decimal(5210.0), Decimal(0.0), Decimal(-100), Decimal(15630.0), Decimal(0)),
        (
            None,
            Decimal(65413.0),
            Decimal(54122.0),
            Decimal(1120.0),
            Decimal(-97.93),
            Decimal(65413.0),
            Decimal(1353.65581464),
        ),
        (None, Decimal(0.0), Decimal(0.0), Decimal(0.0), Decimal(0), Decimal(0), Decimal(0)),
        (1.0, None, Decimal(0.0), Decimal(0.0), Decimal(0), Decimal(0), Decimal(0)),
    ],
)
def test_profit_with_valid_transaction(
    test_session,
    transaction_on_database,
    mocker,
    quantity,
    amount,
    price_on_purchase,
    current_price,
    expected_profit,
    expected_buy_value,
    expected_current_value,
):
    transaction = transaction_on_database(quantity, amount, price_on_purchase)
    print(transaction.__dict__)
    wallet_service = WalletService()

    mocker.patch.object(wallet_service.price_service, "get_price_by_date_time", return_value=current_price)

    response = wallet_service.profit(
        test_session, transaction.uuid, UserResponse(id=1, email="user@test.com", name="User")
    )

    assert response.crypto.symbol == "BTC"
    assert response.profit.buy_date == transaction.date
    assert response.profit.buy_price == transaction.price_on_purchase
    assert response.profit.compare_date.day == datetime.now().day
    assert response.profit.current_price == current_price
    assert round(response.profit.buy_value, 8) == round(expected_buy_value, 8)
    assert round(response.profit.current_value, 8) == round(expected_current_value, 8)
    assert round(response.profit.profit, 2) == round(expected_profit, 2)


def test_profit_with_invalid_transaction(test_session, mocker):
    wallet_service = WalletService()

    with pytest.raises(HTTPException) as exc_info:
        wallet_service.profit(test_session, uuid4(), UserResponse(id=1, email="user@test.com", name="User"))

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Transaction not found"
