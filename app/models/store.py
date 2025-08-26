"""
상점 모델
"""
from sqlalchemy import Column, BigInteger, String, Time, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Store(Base):
    __tablename__ = "store"
    
    storeid = Column(BigInteger, primary_key=True, autoincrement=True)
    marketid = Column(BigInteger, ForeignKey("market.marketid"), nullable=False)
    categoryid = Column(BigInteger, ForeignKey("storecategory.storeCategoryid"), nullable=False)
    hostID = Column(BigInteger, ForeignKey("host.hostID"), nullable=False)
    storeName = Column(String(100), nullable=False)
    tel = Column(String(20), nullable=True)
    dayOpenTime = Column(Time, nullable=True)
    dayCloseTime = Column(Time, nullable=True)
    weekendOpenTime = Column(Time, nullable=True)
    weekendCloseTime = Column(Time, nullable=True)
    address = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    
    # 관계 정의
    market = relationship("Market", back_populates="stores")
    category = relationship("StoreCategory", back_populates="stores")
    host = relationship("Host", back_populates="stores")
    feeds = relationship("Feed", back_populates="store")
    subscriptions = relationship("Subscription", back_populates="store")
