"""
피드 모델 (통합 피드 시스템)
"""
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class PromoKind(enum.Enum):
    store = "store"
    product = "product" 
    event = "event"

class MediaType(enum.Enum):
    image = "image"
    video = "video"

class Feed(Base):
    __tablename__ = "feed"
    
    feedid = Column(BigInteger, primary_key=True, autoincrement=True)
    storeid = Column(BigInteger, ForeignKey("store.storeid"), nullable=False)
    promoKind = Column(Enum(PromoKind), nullable=False)
    mediaType = Column(Enum(MediaType), nullable=False)
    prompt = Column(Text, nullable=True)  # AI 이미지 생성용 프롬프트
    mediaUrl = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # 관계 정의
    store = relationship("Store", back_populates="feeds")
    store_feed = relationship("StoreFeed", back_populates="feed", uselist=False)
    product_feed = relationship("ProductFeed", back_populates="feed", uselist=False)
    event_feed = relationship("EventFeed", back_populates="feed", uselist=False)
    feedlikes = relationship("FeedLike", back_populates="feed")
    reviews = relationship("Review", back_populates="feed")
