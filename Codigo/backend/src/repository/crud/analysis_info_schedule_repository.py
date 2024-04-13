from sqlalchemy.orm import Session

from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel
from src.utilities.runtime import show_runtime


@show_runtime
def get_last_update(db: Session) -> AnalysisInfoScheduleModel | None:
    return db.query(AnalysisInfoScheduleModel).order_by(AnalysisInfoScheduleModel.id.desc()).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[AnalysisInfoScheduleModel]:
    return (
        db.query(AnalysisInfoScheduleModel)
        .order_by(AnalysisInfoScheduleModel.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
