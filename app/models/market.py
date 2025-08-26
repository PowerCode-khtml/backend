"""
마켓 모델
"""
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.database import Base

class Market(Base):
    __tablename__ = "market"
    
    marketid = Column(BigInteger, primary_key=True, autoincrement=True)
    marketName = Column(String(50), nullable=True)
    address = Column(String(255), nullable=True)
    
    # 관계 정의
    stores = relationship("Store", back_populates="market")
