from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel


def get_all(db: Session) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).all()


def get_by_symbol(db: Session, symbol: CurrencyBaseInfoModel) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_currency == symbol.uuid).all()


def save_all(db: Session, closing_prices: list[FirstStageAnalysisModel]) -> list[FirstStageAnalysisModel]:
    db.add_all(closing_prices)
    db.commit()
    for closing_price in closing_prices:
        db.refresh(closing_price)
    return closing_prices
