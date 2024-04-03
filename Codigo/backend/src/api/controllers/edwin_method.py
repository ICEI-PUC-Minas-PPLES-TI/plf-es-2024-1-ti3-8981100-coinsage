from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.dependencies.session import get_db
from src.models.schemas.analysis_info import AnalysisInfoResponse
from src.services.analysis_collector import AnalysisCollector

router = APIRouter(
    prefix="/edwin_method",
    tags=["edwin_method"]
)


@router.get(
    path="/",
    name="edwin_method:read-last-analysis",
    response_model=str,
    description="Coletar dados da última análise.",
    status_code=status.HTTP_200_OK,
)
async def get_accounts(db: Session = Depends(get_db)) -> AnalysisInfoResponse:
  analysis = AnalysisCollector(session=db).collect_symbols_info()
  return analysis

#async def get_accounts(db: Session = Depends(get_db)) -> CurrencyInfoResponse:   
    #if not scheduler.running:
   #     scheduler.start_schedules(db)     
   # CurrenciesLogoCollector(session=db).collect_symbols_info()
    #analysis = CurrenciesLogoCollector(session=db).get_cryptos()
  #  return analysis

#Os schedules não vão depender de nada para rodar. Eles tem que rodar sozinho no horário definido. (update_currencies_info)
  #Porém eu preciso fazer isso iniciar
  #Definido na main
  
#A análise por enquanto só vai retornar os status dos schedules ( qual foi a última vez que atualizou e qual vai ser a próxima análise) e os dados da moeda (que é a logo e o nome)

#PASSOS
  #Fazer a rota no controller
  #No service você só vai pegar os dados da moeda de fato (inicialmente não há esquema de banco de dados, ele só vai linkar com a outra tabela, não precisa replicar esse dado numa tabela de novo). Tabela de análises que vai ter Foreign key de outra tabela para pegar esses dados da moeda
     #Então é só fazer o controller retornar aquele json e cadastrar o schedule dele também (update_currencies_info.py)
     