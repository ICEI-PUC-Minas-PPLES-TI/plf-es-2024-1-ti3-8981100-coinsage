from typing import List

from loguru import logger
from sqlalchemy import func, select, Uuid
from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.models.schemas.generic_pagination import PaginatedResponse
from src.utilities.runtime import show_runtime


def get_all(db: Session) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).all()


@show_runtime
def get_by_analysis_uuid(db: Session, uuid: str) -> list[FirstStageAnalysisModel]:
    return db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_analysis == uuid).all()


def get_paginated_by_uuid(
    db: Session, uuid: Uuid, limit: int, offset: int
) -> tuple[list[FirstStageAnalysisModel], PaginatedResponse]:
    items_query = (
        select(FirstStageAnalysisModel)
        .where(FirstStageAnalysisModel.uuid_analysis == uuid)
        .limit(limit)
        .offset(offset)
    )
    items = db.execute(items_query).scalars().all()
    count = db.scalar(select(func.count()).where(FirstStageAnalysisModel.uuid_analysis == uuid))
    remaining = max(count - (limit + offset), 0)  # type: ignore

    return items, PaginatedResponse(total=count, remaining=remaining, page=limit if count > limit else count)  # type: ignore


def get_by_symbol(db: Session, symbol: CurrencyBaseInfoModel, analysis_uuid: Uuid) -> FirstStageAnalysisModel | None:
    found = db.query(FirstStageAnalysisModel).filter(
        FirstStageAnalysisModel.uuid_currency == symbol.uuid and FirstStageAnalysisModel.uuid_analysis == analysis_uuid
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
