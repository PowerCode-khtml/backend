"""
사용자 모델
"""
from sqlalchemy import Column, BigInteger, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "user"
    
    userid = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    imgUrl = Column(String(255), nullable=True)
    
    # 관계 정의
    subscriptions = relationship("Subscription", back_populates="user")
    feedlikes = relationship("FeedLike", back_populates="user")
    reviews = relationship("Review", back_populates="user")
