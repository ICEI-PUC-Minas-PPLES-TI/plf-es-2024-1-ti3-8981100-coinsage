from openpyxl import Workbook
from typing import List
from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from datetime import datetime

class WorkbookService:
    @staticmethod
    def create_workbook(headers: List[str]) -> Workbook:
        workbook = Workbook()
        worksheet = workbook.active
        for col, header in enumerate(headers, start=1):
            worksheet.cell(row=1, column=col, value=header)
        return workbook

    @staticmethod
    def fill_workbook(workbook: Workbook, data: List[FirstStageAnalysisModel], headers: List[str]) -> Workbook:
        worksheet = workbook.active
        header_to_model_attr = {
            
            "RANKING": "ranking",
            "MARKET CAP": "market_cap",
            "INCREASE DATE": "increase_date",
            "% WEEK INCREASE": "week_increase_percentage",
            "WEEK CLOSING PRICE": "closing_price",
            "WEEK OPEN PRICE": "open_price",
            "WEEK CLOSING PRICE > EMA8(w)": "ema8_less_close",
            "EMA8 > WEEK OPEN PRICE": "ema8_greater_open",
            "EMAs ALIGNED": "ema_aligned",
            "INCREASE VOLUME(d) DATE": "increase_volume_day",
            "INCREASE VOLUME(d)": "week_increase_volume",
            "DAY BEFORE VOLUME(d)": "day_before_volume",
            "% VOLUME/VOLUME DAY BEFORE": "volumes_relation",
            "VOLUME > 200%": "expressive_volume_increase",
            "BUY SIGNAL": "buying_signal",
        }
        for row_idx, item in enumerate(data, start=2):
            for header in headers:
                col_idx = headers.index(header) + 1
                model_attr = header_to_model_attr.get(header)
                if model_attr:
                    value = getattr(item, model_attr)
                    if value is None:
                        value = "N/A"
                    worksheet.cell(row=row_idx, column=col_idx, value=value)
                else:
                    worksheet.cell(row=row_idx, column=col_idx, value="N/A")
        return workbook
