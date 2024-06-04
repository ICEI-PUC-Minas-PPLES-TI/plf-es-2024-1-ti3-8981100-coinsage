from typing import Any, List

from fastapi.encoders import jsonable_encoder
from loguru import logger
from sqlalchemy import func, select, union, Uuid
from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.models.schemas.analysis.first_stage_analysis import VolumeAnalysis
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
    # if offset == 0:
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
    items = sorted(items, key=lambda x: (x.week_increase_percentage is None, x.week_increase_percentage), reverse=True)  # type: ignore
    items = [items.pop(items.index(specific_item))] + items if specific_item is not None else items  # type: ignore
    # else:
    #     items_query = (
    #         select(FirstStageAnalysisModel)
    #         .order_by(FirstStageAnalysisModel.week_increase_percentage.desc())
    #         .where(FirstStageAnalysisModel.uuid_analysis == uuid)
    #         .limit(limit)
    #         .offset(offset)
    #     )

    #     items = db.execute(items_query).scalars().all()
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


def update_current_price(
    db: Session, symbols_current_price: list[dict], analysis_indentifier: Uuid
) -> list[FirstStageAnalysisModel]:
    update_current_price_encoded: list[Any] = []
    if symbols_current_price is None:
        raise ValueError(f"Failed to get current price for the symbols")
    for current_price in symbols_current_price:
        currency_info = db.execute(
            select(CurrencyBaseInfoModel).where(CurrencyBaseInfoModel.symbol == current_price["symbol"])  # type:ignore
        ).scalar()

        if currency_info:
            first_stage = db.execute(
                select(FirstStageAnalysisModel)
                .where(FirstStageAnalysisModel.uuid_analysis == analysis_indentifier)
                .where(FirstStageAnalysisModel.uuid_currency == currency_info.uuid)
            ).scalar()

            new_analysis = FirstStageAnalysisModel(
                uuid_analysis=analysis_indentifier,
                uuid_currency=currency_info.uuid,
                current_price=current_price["price"],  # type:ignore
            )

            first_stage.current_price = current_price["price"]  # type:ignore
            db.commit()
            # db.add(new_analysis)
        else:
            logger.info(f"Moeda com símbolo {current_price['symbol']} não encontrada.")  # type:ignore
        # update_current_price_encoded.append(jsonable_encoder(first_stage))
        # db.commit()
        db.close()

    return update_current_price_encoded


def add_volume_analysis(db: Session, volume_analysis_data: List[VolumeAnalysis], analysis_indentifier: Uuid) -> None:
    try:
        for data in volume_analysis_data:
            currency_info = db.execute(
                select(CurrencyBaseInfoModel).where(CurrencyBaseInfoModel.symbol == data["symbol"])
            ).scalar()

            if currency_info:
                first_stage = db.execute(
                    select(FirstStageAnalysisModel)
                    .where(FirstStageAnalysisModel.uuid_analysis == analysis_indentifier)
                    .where(FirstStageAnalysisModel.uuid_currency == currency_info.uuid)
                ).scalar()

                first_stage.volume_before_increase = data["volume_before_increase"]
                first_stage.increase_volume_day = data["increase_volume_day"]
                first_stage.expressive_volume_increase = data["expressive_volume_increase"]
                first_stage.increase_volume = data["increase_volume"]
                first_stage.today_volume = data["today_volume"]

                db.commit()
            else:
                logger.info(f"Moeda com símbolo {data['symbol']} não encontrada.")
    except Exception as e:
        db.rollback()
        logger.info(f"Erro ao adicionar análises: {e}")
    finally:
        db.close()


def update_ranking(db: Session, symbol: str, new_ranking: int, analysis_uuid: Uuid):
    entry = (
        db.query(FirstStageAnalysisModel)
        .join(CurrencyBaseInfoModel, FirstStageAnalysisModel.uuid_currency == CurrencyBaseInfoModel.uuid)
        .filter(CurrencyBaseInfoModel.symbol == symbol, FirstStageAnalysisModel.uuid_analysis == analysis_uuid)
        .first()
    )

    if entry:
        entry.ranking = new_ranking
        db.commit()
        # logger.info(f"Updated ranking to {new_ranking} for symbol {symbol} in analysis {analysis_uuid}.")
        return entry
    else:
        logger.error(f"Currency with symbol {symbol} and analysis UUID {analysis_uuid} not found.")
        return None
