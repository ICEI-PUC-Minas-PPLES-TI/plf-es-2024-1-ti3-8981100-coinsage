from sqlalchemy.orm import Session

from src.models.db.currencies_info_schedule import CurrenciesInfoScheduleModel


def get_last_update(db: Session) -> CurrenciesInfoScheduleModel | None:
    return db.query(CurrenciesInfoScheduleModel).order_by(CurrenciesInfoScheduleModel.id.desc()).first()


def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[CurrenciesInfoScheduleModel]:
    return (
        db.query(CurrenciesInfoScheduleModel)
        .order_by(CurrenciesInfoScheduleModel.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
