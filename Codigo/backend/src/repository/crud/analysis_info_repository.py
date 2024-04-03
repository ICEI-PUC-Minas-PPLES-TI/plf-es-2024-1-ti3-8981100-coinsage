from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db import analysis
from src.models.schemas import analysis_info


def get_crypto(db: Session, crypto_uuid: Uuid) -> analysis.AnalysisBaseInfoModel | None:
    return (
        db.query(analysis.AnalysisBaseInfoModel)
        .filter(analysis.AnalysisBaseInfoModel.uuid == crypto_uuid)
        .first()
    )


def get_analysis_info_by_uuid(db: Session, uuid_value: Uuid) -> analysis.AnalysisBaseInfoModel | None:
    return (
        db.query(analysis.AnalysisBaseInfoModel)
        .filter(analysis.AnalysisBaseInfoModel.uuid == uuid_value)
        .first()
    )


def get_cryptos(db: Session, skip: int = 0, limit: int = 10000) -> list[analysis.AnalysisBaseInfoModel]:
    return db.query(analysis.AnalysisBaseInfoModel).offset(skip).limit(limit).all()


def get_analysis_info_by_symbol(db: Session, symbol: str) -> analysis.AnalysisBaseInfoModel | None:
    return (
        db.query(analysis.AnalysisBaseInfoModel)
        .filter(analysis.AnalysisBaseInfoModel.symbol == symbol)
        .first()
    )


def create_crypto(db: Session, crypto: analysis_info.AnalysisInfo) -> analysis.AnalysisBaseInfoModel:
    currency = analysis.AnalysisBaseInfoModel(
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
    db.query(analysis.AnalysisBaseInfoModel).delete()
