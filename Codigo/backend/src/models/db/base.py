from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base


class BaseModel(object):
    created_at = Column(DateTime, default=datetime.now())
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


Base = declarative_base(cls=BaseModel)
