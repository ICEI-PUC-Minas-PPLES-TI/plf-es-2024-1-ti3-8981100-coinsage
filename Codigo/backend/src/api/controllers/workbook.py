from openpyxl import Workbook
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from src.api.dependencies.session import get_db
from src.services.workbook.workbook_service import WorkbookService
from src.repository.crud.first_stage_repository import get_all
import os

router = APIRouter(prefix="/workbook", tags=["Workbook"])

@router.get("/generate", response_class=FileResponse)
async def generate_workbook(db: Session = Depends(get_db)):
    # Cabeçalhos da planilha
    headers = [
        "RANKING",
        "MARKET CAP",
        "INCREASE DATE",
        "% WEEK INCREASE",
        "WEEK CLOSING PRICE",
        "WEEK OPEN PRICE",
        "WEEK CLOSING PRICE > EMA8(w)",
        "EMA8 > WEEK OPEN PRICE",
        "EMAs ALIGNED",
        "INCREASE VOLUME(d) DATE",
        "INCREASE VOLUME(d)",
        "DAY BEFORE VOLUME(d)",
        "% VOLUME/VOLUME DAY BEFORE",
        "VOLUME > 200%",
        "BUY SIGNAL",
    ]
    
    # obtendo dados do banco
    data = get_all(db)
    
    # criando e preenchendo planilha
    workbook = WorkbookService.create_workbook(headers)
    filled_workbook = WorkbookService.fill_workbook(workbook, data, headers)
    
    # Salvando
    file_path = "workbook.xlsx"
    filled_workbook.save(file_path)
    
    # Retornando arquivo como resposta
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="workbook.xlsx", media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    else:
        raise HTTPException(status_code=404, detail="File not found.")
