"""
상점 피드 상세 모델
"""
from sqlalchemy import Column, BigInteger, Text, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class StoreFeed(Base):
    __tablename__ = "storefeed"
    
    feedid = Column(BigInteger, ForeignKey("feed.feedid"), primary_key=True)
    description = Column(Text, nullable=True)
    imgUrl = Column(String(255), nullable=False)
    
    # 관계 정의
    feed = relationship("Feed", back_populates="store_feed")
