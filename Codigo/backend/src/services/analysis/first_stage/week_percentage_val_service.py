from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from loguru import logger
from concurrent.futures import ThreadPoolExecutor

from src.models.db.first_stage_analysis import FirstStageAnalysisModel
from src.services.analysis.first_stage.closing_price_service import ClosingPriceService
from src.utilities.runtime import show_runtime
from src.repository.crud import first_stage_repository

class WeekPercentageValorizationService:
    def __init__(self,
                 session: Session, 
                 closing_price_service: Annotated[ClosingPriceService, Depends(ClosingPriceService)]):
        self.session = session
        self.closing_price_service = closing_price_service
        self.repository = first_stage_repository
        
    def _calculate_week_percentage_valorization(self, symbol: str) -> float:
        last_weeks_closing_prices: list[FirstStageAnalysisModel] = self.closing_price_service.get_closing_price_by_symbol(symbol)
        
        if last_weeks_closing_prices.__len__() < 2:
            logger.warning(f"Closing prices not found for symbol {symbol}")
            raise ValueError(f"Closing prices not found for symbol {symbol}")
        
        current_week = last_weeks_closing_prices[1]
        last_week = last_weeks_closing_prices[0]
        percentage_diff = (current_week.closing_price - last_week.closing_price) / last_week.closing_price * 100
        # logger.info(f"Closing prices compare [{symbol}]: {float(percentage_diff)}%")
        return float(percentage_diff)
    
    @show_runtime
    def calculate_all_week_percentage_valorization(self, symbols: list[str]):
        all_diffs = []
        
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._calculate_week_percentage_valorization, symbol) for symbol in symbols]
            
            for future, symbol in zip(futures, symbols):
                collected = future.result()
                all_diffs.append({symbol: collected})
        
        # update first stage model with week percentage valorization
        self.update_last(all_diffs)
        
        return self
        
    @show_runtime
    def update_last(self, increases):
        for increase in increases:
            symbol = list(increase.keys())[0]
            week_percentage = increase[symbol]
            self.repository.update_last_week_percentage(self.session, symbol, week_percentage)