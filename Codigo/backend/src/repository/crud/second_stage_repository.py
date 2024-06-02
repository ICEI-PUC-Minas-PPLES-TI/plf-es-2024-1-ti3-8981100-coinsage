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
                second_stage = db.execute(
                    select(SecondStageAnalysisModel)
                    .where(SecondStageAnalysisModel.uuid_analysis == analysis_indentifier)
                    .where(SecondStageAnalysisModel.uuid_currency == currency_info.uuid)
                ).scalar()

                second_stage.year_variation_per = data["year_variation_per"]
                second_stage.semester_variation_per = data["semester_variation_per"]
                second_stage.quarter_variation_per = data["quarter_variation_per"]
                second_stage.month_variation_perdata["month_variation_per"]
                second_stage.week_variation_per = data["week_variation_per"]
                second_stage.variation_greater_bitcoin = data["variation_greater_bitcoin"]

                db.commit()
            else:
                logger.info(f"Moeda com símbolo {data['symbol']} não encontrada.")
    except Exception as e:
        db.rollback()
        logger.info(f"Erro ao adicionar análises: {e}")
    finally:
        db.close()
