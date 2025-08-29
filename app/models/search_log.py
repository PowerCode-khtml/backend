from sqlalchemy import Column, String, Integer
from app.database import Base

class SearchLog(Base):
    __tablename__ = "search_log"

    keyword = Column(String(100), primary_key=True, nullable=False)
    volume = Column(Integer, nullable=False, server_default='0')
