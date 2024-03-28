from sqlalchemy.orm import Session

from src.models.db.analysis.closing_price_model import ClosingPriceModel
from src.models.db.currency_base_info import CurrencyBaseInfoModel


def get_all(db: Session) -> list[ClosingPriceModel]:
    return db.query(ClosingPriceModel).all()


def get_by_symbol(db: Session, symbol: CurrencyBaseInfoModel) -> list[ClosingPriceModel]:
    return db.query(ClosingPriceModel).filter(ClosingPriceModel.uuid_currency_info == symbol.uuid).all()


def save_all(db: Session, closing_prices: list[ClosingPriceModel]) -> list[ClosingPriceModel]:
    db.add_all(closing_prices)
    db.commit()
    for closing_price in closing_prices:
        db.refresh(closing_price)
    return closing_prices
