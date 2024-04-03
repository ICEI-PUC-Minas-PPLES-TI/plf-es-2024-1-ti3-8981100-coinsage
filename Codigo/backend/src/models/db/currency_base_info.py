import uuid

from sqlalchemy import Column, Integer, String, Text, UUID, Float
from sqlalchemy.orm import validates

from .base import Base


class CurrencyBaseInfoModel(Base):
    __tablename__ = "currency_base_info"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(length=100), unique=True)
    cmc_id = Column(Integer)
    cmc_slug = Column(String(length=100))
    logo = Column(String(length=1000))
    name = Column(String(length=100))
    description = Column(String(length=5000))
    current_price = Column(Float)
    _technical_doc = Column(Text, nullable=True)
    _urls = Column(Text, nullable=True)

    @property
    def technical_doc(self):
        if self._technical_doc:
            return self._technical_doc.split(",")
        else:
            return []

    @technical_doc.setter
    def technical_doc(self, value: list[str]):
        if isinstance(value, list):
            for doc in value:
                if not isinstance(doc, str) or len(doc) > 1000:
                    raise ValueError("Each element in technical_doc must be a string of at max 1000 chars")

            self._technical_doc = ",".join(value)  # type: ignore
        else:
            raise ValueError("technical_doc must be a list of strings")

    @property
    def urls(self):
        if self._urls:
            return self._urls.split(",")
        else:
            return []

    @urls.setter
    def urls(self, value: list[str]):
        if isinstance(value, list):
            for doc in value:
                if not isinstance(doc, str) or len(doc) > 1000:
                    raise ValueError("Each element in technical_doc must be a string of at max 1000 chars")

            self._urls = ",".join(value)  # type: ignore
        else:
            raise ValueError("urls must be a list of strings")

    @validates("technical_doc", "urls")
    def validate_list(self, key, value):
        if not isinstance(value, list):
            raise ValueError(f"{key} must be a list of strings")
        return value
