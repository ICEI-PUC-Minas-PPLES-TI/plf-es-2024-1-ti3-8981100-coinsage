from typing import List

from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db import currency_base_info
from src.models.db.rel_setor_currency_base_info import SetorCurrencyBaseInfo
from src.models.schemas import currency_info
from src.utilities.runtime import show_runtime


def get_crypto(db: Session, crypto_uuid: Uuid) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.uuid == crypto_uuid)
        .first()
    )


def get_currency_info_by_uuid(db: Session, uuid_value: Uuid) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.uuid == uuid_value)
        .first()
    )


def get_cryptos(db: Session, skip: int = 0, limit: int = 10000) -> list[currency_base_info.CurrencyBaseInfoModel]:
    return db.query(currency_base_info.CurrencyBaseInfoModel).all()


def get_currency_info_by_symbol(db: Session, symbol: str) -> currency_base_info.CurrencyBaseInfoModel | None:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .filter(currency_base_info.CurrencyBaseInfoModel.symbol == symbol)
        .first()
    )


def create_crypto(db: Session, crypto: currency_info.CurrencyInfo) -> currency_base_info.CurrencyBaseInfoModel:
    currency = currency_base_info.CurrencyBaseInfoModel(
        symbol=crypto.symbol,
        cmc_id=crypto.cmc_id,
        cmc_slug=crypto.cmc_slug,
        logo=crypto.logo,
        name=crypto.name,
        description=crypto.description,
        technical_doc=crypto.technical_doc,
        urls=crypto.urls,
    )
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency


def clear_table(db: Session) -> None:
    db.query(currency_base_info.CurrencyBaseInfoModel).delete()


def get_coins_by_sector(db: Session, sector_uuid: Uuid) -> List[currency_base_info.CurrencyBaseInfoModel]:
    return (
        db.query(currency_base_info.CurrencyBaseInfoModel)
        .join(
            SetorCurrencyBaseInfo, SetorCurrencyBaseInfo.uuid_currency == currency_base_info.CurrencyBaseInfoModel.uuid
        )
        .filter(SetorCurrencyBaseInfo.uuid_setor == sector_uuid)
        .all()
    )
