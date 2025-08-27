"""
리뷰 모델
"""
from sqlalchemy import Column, BigInteger, Text, String, Integer, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Review(Base):
    __tablename__ = "review"
    
    reviewid = Column(BigInteger, primary_key=True, autoincrement=True)
    userid = Column(BigInteger, ForeignKey("user.userid"), nullable=False)
    feedid = Column(BigInteger, ForeignKey("feed.feedid"), nullable=False)
    content = Column(Text, nullable=False)
    imgUrl = Column(String(255), nullable=True)
    rating = Column(Integer, nullable=False)  # 1-5 평점
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # 관계 정의
    user = relationship("User", back_populates="reviews")
    feed = relationship("Feed", back_populates="reviews")

    # 테이블 제약 조건
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='chk_review_rating'),
    )
