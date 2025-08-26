"""
피드 좋아요 모델
"""
from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class FeedLike(Base):
    __tablename__ = "feedlike"
    
    userid = Column(BigInteger, ForeignKey("user.userid"), primary_key=True)
    feedid = Column(BigInteger, ForeignKey("feed.feedid"), primary_key=True)
    
    # 관계 정의
    user = relationship("User", back_populates="feedlikes")
    feed = relationship("Feed", back_populates="feedlikes")
