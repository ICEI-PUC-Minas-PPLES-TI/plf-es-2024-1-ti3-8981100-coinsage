from typing import List

from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.models.schemas.analysis.first_stage_analysis import FirstStageAnalysisResponse
from src.utilities.runtime import show_runtime


def get_all(db: Session) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).all()


@show_runtime
def get_by_analysis_uuid(db: Session, uuid: str) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_analysis == uuid).all()


def get_client_formated(db: Session, uuid: Uuid) -> List[FirstStageAnalysisResponse]:  # type: ignore
    pass


def get_by_symbol(db: Session, symbol: CurrencyBaseInfoModel, analysis_uuid: Uuid) -> FirstStageAnalysisModel | None:
    found = db.query(FirstStageAnalysisModel).filter(
        FirstStageAnalysisModel.uuid_currency == symbol.uuid and FirstStageAnalysisModel.uuid_analysis == analysis_uuid
    )

    for founded in found:
        logger.debug(
            f"""
                     Founded symbol: {founded.uuid_currency}
                     Founded analysis: {founded.uuid_analysis}
                     """
        )

    return found.one_or_none()


def update_last_week_percentage(db: Session, symbol: str, week_percentage: float, uuid_analysis: Uuid):
    item = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol, FirstStageAnalysisModel.uuid_analysis == uuid_analysis)
        .one_or_none()
    )

    if item is None:
        raise ValueError(f"Item not found for symbol {symbol}")

    item.week_increase_percentage = week_percentage  # type: ignore
    db.commit()


def save_all(db: Session, closing_prices: list[FirstStageAnalysisModel]):
    db.add_all(closing_prices)
    db.commit()
    # for closing_price in closing_prices:
    #     db.refresh(closing_price)
    # return closing_prices


def update_current_price(db: Session, symbol: str, current_price: float | None) -> FirstStageAnalysisModel:
    """
    Update the current price of a currency symbol in the database.

    Args:
        db (Session): SQLAlchemy database session.
        symbol (str): The symbol of the currency.
        current_price (float): The current price to be updated.

    Raises:
        ValueError: If the current_price is None or if no item is found for the given symbol.

    Returns:
        FirstStageAnalysisModel
    """
    if current_price is None:
        raise ValueError(f"Failed to get current price for symbol {symbol}")

    item = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol)
        .order_by(FirstStageAnalysisModel.today.desc())
        .first()
    )

    if item is None:
        raise ValueError(f"Item not found for symbol {symbol}")

    update_current_price_encoded = jsonable_encoder(item)

    item.current_price = current_price
    db.commit()
    return update_current_price_encoded
