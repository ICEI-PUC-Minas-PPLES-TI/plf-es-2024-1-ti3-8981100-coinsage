from typing import List

from loguru import logger
from sqlalchemy import select, Uuid
from sqlalchemy.orm import Session

from src.models.db.currency_base_info import CurrencyBaseInfoModel
from src.models.db.second_stage_analysis import SecondStageAnalysisModel
from src.models.schemas.analysis.first_stage_analysis import VolumeAnalysis


def add_variation_analysis(
    db: Session, variation_analysis_data: List[VolumeAnalysis], analysis_indentifier: Uuid
) -> None:
    try:
        for data in variation_analysis_data:
            currency_info = db.execute(
                select(CurrencyBaseInfoModel).where(CurrencyBaseInfoModel.symbol == data["symbol"])
            ).scalar()

            if currency_info:
                new_analysis = SecondStageAnalysisModel(
                    uuid_analysis=analysis_indentifier,
                    uuid_currency=currency_info.uuid,
                    year_variation_per=data["year_variation_per"],
                    semester_variation_per=data["semester_variation_per"],
                    quarter_variation_per=data["quarter_variation_per"],
                    month_variation_per=data["month_variation_per"],
                    week_variation_per=data["week_variation_per"],
                    variation_greater_bitcoin=data["variation_greater_bitcoin"],
                )

                db.commit()
                db.add(new_analysis)
            else:
                logger.info(f"Moeda com símbolo {data['symbol']} não encontrada.")
        db.commit()
    except Exception as e:
        db.rollback()
        logger.info(f"Erro ao adicionar análises: {e}")
    finally:
        db.close()
