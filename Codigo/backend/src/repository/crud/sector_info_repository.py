from typing import Optional

from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db.rel_setor_currency_base_info import SetorCurrencyBaseInfo
from src.models.db.setor import Setor


def get_sector_by_cmc_id(db: Session, cmc_id: int) -> Optional[Setor]:
    return db.query(Setor).filter(Setor.cmc_id == cmc_id).first()


def deactivate_sector(db: Session, sector: Setor) -> Setor:
    sector.active = False  # type: ignore
    db.commit()
    db.refresh(sector)
    return sector


def create_sector(db: Session, sector: Setor) -> Setor:
    db.add(sector)
    db.commit()
    db.refresh(sector)
    return sector


def update(db: Session, sector: Setor) -> Setor:
    db.commit()
    db.refresh(sector)
    return sector


def add_coin_to_sector(db: Session, relation: SetorCurrencyBaseInfo) -> SetorCurrencyBaseInfo:
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


def remove_all_coins_from_sector(db: Session, sector: Setor):
    db.query(SetorCurrencyBaseInfo).filter(SetorCurrencyBaseInfo.uuid_setor == sector.uuid).delete()
