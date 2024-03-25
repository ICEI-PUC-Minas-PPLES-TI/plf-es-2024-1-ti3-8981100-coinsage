# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from sqlalchemy.orm import Session
# from loguru import logger

# scheduler = AsyncIOScheduler()

# db = None

# def start_schedules(app_db: Session):
#     global db
#     db = app_db
#     scheduler.start()
#     logger.info("Schedules started")
    
# def stop_schdeules():
#     scheduler.shutdown()
#     logger.info("Schedules stopped")