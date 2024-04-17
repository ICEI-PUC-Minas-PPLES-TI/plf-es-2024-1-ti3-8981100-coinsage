from typing import Optional

from sqlalchemy import func, select, Uuid
from sqlalchemy.orm import Session

from src.models.db import analysis
from src.utilities.runtime import show_runtime


@show_runtime
def get_last(db: Session) -> Optional[analysis.Analysis]:
    return db.query(analysis.Analysis).order_by(analysis.Analysis.date.desc()).first()


@show_runtime
def get_analysis_info_by_uuid(db: Session, uuid_value: Uuid) -> analysis.Analysis | None:
    return db.query(analysis.Analysis).filter(analysis.Analysis.uuid == uuid_value).first()
