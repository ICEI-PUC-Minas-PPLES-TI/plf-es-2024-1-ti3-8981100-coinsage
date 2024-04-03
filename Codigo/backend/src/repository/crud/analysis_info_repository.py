from typing import Optional

from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.models.db import analysis
from src.models.schemas.analysis import analysis_info


def get_last(db: Session) -> Optional[analysis.Analysis]:
    return db.query(analysis.Analysis).order_by(analysis.Analysis.date.desc()).first()


def get_analysis_info_by_uuid(db: Session, uuid_value: Uuid) -> analysis.Analysis | None:
    return db.query(analysis.Analysis).filter(analysis.Analysis.uuid == uuid_value).first()
