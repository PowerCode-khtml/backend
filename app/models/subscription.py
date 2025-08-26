"""
구독 모델
"""
from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Subscription(Base):
    __tablename__ = "subscription"
    
    userid = Column(BigInteger, ForeignKey("user.userid"), primary_key=True)
    storeid = Column(BigInteger, ForeignKey("store.storeid"), primary_key=True)
    
    # 관계 정의
    user = relationship("User", back_populates="subscriptions")
    store = relationship("Store", back_populates="subscriptions")
