from typing import List

from loguru import logger
from sqlalchemy import func, select, union, Uuid
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
    if offset == 0:
        query_btc = (
            select(FirstStageAnalysisModel)
            .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
            .where(FirstStageAnalysisModel.uuid_analysis == uuid)
            .where(CurrencyBaseInfoModel.symbol == "BTC")
            .limit(1)
            .offset(0)
        )
        specific_item = db.execute(query_btc).scalars().first()

        items_query_regular = (
            select(FirstStageAnalysisModel)
            .order_by(FirstStageAnalysisModel.week_increase_percentage.desc())
            .where(FirstStageAnalysisModel.uuid_analysis == uuid)
            .where(FirstStageAnalysisModel.uuid_currency != specific_item.uuid_currency if specific_item is not None else None)  # type: ignore
            .limit(limit - 1 if specific_item is not None else limit)  # Remaining limit after the specific item
            .offset(offset)
        )

        queried = db.execute(items_query_regular).scalars().all()

        items = list(set([specific_item] + queried)) if specific_item is not None else queried  # type: ignore
        items = sorted(items, key=lambda x: x.week_increase_percentage, reverse=True)  # type: ignore
    else:
        items_query = (
            select(FirstStageAnalysisModel)
            .order_by(FirstStageAnalysisModel.week_increase_percentage.desc())
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
        FirstStageAnalysisModel.uuid_currency == symbol.uuid, FirstStageAnalysisModel.uuid_analysis == analysis_uuid
    )

    return found.first()


def get_by_symbol_str(db: Session, symbol: str, analysis_uuid: Uuid) -> FirstStageAnalysisModel | None:
    found = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol, FirstStageAnalysisModel.uuid_analysis == analysis_uuid)
    )

    return found.first()


def update_last_week_percentage(db: Session, symbol: str, week_percentage: float, uuid_analysis: Uuid):
    item = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol, FirstStageAnalysisModel.uuid_analysis == uuid_analysis)
        .first()
    )

    if item is None:
        raise ValueError(f"Item not found for symbol {symbol}")

    item.week_increase_percentage = week_percentage  # type: ignore
    db.commit()


def delete_not_ended(db: Session, uuid_analysis: Uuid):
    db.query(FirstStageAnalysisModel).filter(FirstStageAnalysisModel.uuid_analysis == uuid_analysis).delete()
    db.commit()


def save_all(db: Session, closing_prices: list[FirstStageAnalysisModel]):
    db.add_all(closing_prices)
    db.commit()
    # for closing_price in closing_prices:
    #     db.refresh(closing_price)
    # return closing_prices
