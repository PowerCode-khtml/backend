"""
호스트 모델
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Host(Base):
    __tablename__ = "host"
    
    hostID = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    imgUrl = Column(String(255), nullable=True)
    
    # 관계 정의
    stores = relationship("Store", back_populates="host")
