"""
이벤트 피드 상세 모델
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class EventFeed(Base):
    __tablename__ = "eventfeed"
    
    feedid = Column(BigInteger, ForeignKey("feed.feedid"), primary_key=True)
    eventName = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    imgUrl = Column(String(255), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    
    # 관계 정의
    feed = relationship("Feed", back_populates="event_feed")
