import datetime
#import schedule
#biblioteca schedule permite agendar tarfeas em intervalos específicos
#from croniter import croniter
#módulo croniter permite calcular o próximo momente de execução com base na expressão cron
from src.config.manager import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from sqlalchemy.orm import Session

from src.models.db.analysis_info_schedule import AnalysisInfoScheduleModel



scheduler = AsyncIOScheduler()

db = None


#scheduler.add_job(update_analysis_info, "cron", hour=8, minute=0 )

#scheduler.start()

#!
#todo CHECK UPDATES

@scheduler.scheduled_job(
    "cron",
    hour=settings.SCHEDULES["update_currencies_info"]["hour"],
    minute=settings.SCHEDULES["update_currencies_info"]["minute"],
    second=settings.SCHEDULES["update_currencies_info"]["second"],
    id="update_analysis_info",
)

##todo TABELA ANALISE ESPECÍFICA QUE RODOU EM UM DIA ESPECIFICO  -- isso que vai ser a tabela da analysis

#todo Então quando o Job rodar, ele deve ir e criar essa tabela de análise ali.


def update_analysis_info():
    print("Puxe tudo aqui")
    logger.info("Updating analysis info")
    if db is not None:
        func_session: Session = db
        #! analysis_currency_stage_one | analysis_currency_stage_two | analysis_currency_stage_three | analysis_currency_stage_four    --> Utilizando a currency_base_info        
        CurrenciesLogoCollector(session=func_session).collect_symbols_info()
    else:
        logger.critical("Database session is not available")
        
        
        
def check_update_analysis_info(db: Session, settings: dict) -> None:
    next_update_time = (
        db.query(AnalysisInfoScheduleModel).order_by(AnalysisInfoScheduleModel.next_scheduled_time.desc()).first()
    )
    now: datetime = datetime.now()
    settings_time: datetime = now.replace(hour=settings["hour"], minute=settings["minute"], second=settings["second"])

    if next_update_time is not None:
        if next_update_time.last_update_time.date() == now.date():
            logger.info("Currencies info already updated today")
            return

        logger.info("Schedule is late. Updating now")
        update_analysis_info(db=db)
        return

    if settings_time < now:
        logger.info("Schedule never ran. Updating now")
        update_analysis_info(db=db)












'''async def get_analysis():
      print("Boss Wake Up")

scheduler = AsyncIOScheduler()'''
#função scheduler usada para agendar uma tarefa assíncrona para ser executada em determinado horário
    #necessita dois argumentos:
     #tarefa que será executada e horário incicando quando a tarefa será executada

'''scheduler.add_job(get_analysis, "cron", day_of_week="mon-sun", hour=21, minute=10)
scheduler.start()'''



#cronjob -> tarefa agendada executada periodicamente 


'''def minha_tarefa():
    print("Executando tarefa...")'''

# Agendar a tarefa para ser executada a cada minuto
'''schedule.every(1).minutes.do(minha_tarefa)'''

# Executar o cronjob indefinidamente
'''while True:
    #schedule.run_pending()
    datetime.sleep(1)
    '''
    

    