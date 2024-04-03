from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel


def get_all(db: Session) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).all()


def get_by_analysis_uuid(db: Session, uuid: str) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_analysis == uuid).all()


def get_by_symbol(db: Session, symbol: CurrencyBaseInfoModel) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_currency == symbol.uuid).all()


def update_last_week_percentage(db: Session, symbol: str, week_percentage: float):
    item = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol)
        .order_by(FirstStageAnalysisModel.today.desc())
        .first()
    )

    if item is None:
        raise ValueError(f"Item not found for symbol {symbol}")

    item.week_increase_percentage = week_percentage  # type: ignore
    db.commit()


def save_all(db: Session, closing_prices: list[FirstStageAnalysisModel]) -> list[FirstStageAnalysisModel]:
    db.add_all(closing_prices)
    db.commit()
    for closing_price in closing_prices:
        db.refresh(closing_price)
    return closing_prices
