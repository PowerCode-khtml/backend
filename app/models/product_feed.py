"""
상품 피드 상세 모델
"""
from sqlalchemy import Column, BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductFeed(Base):
    __tablename__ = "productfeed"
    
    feedid = Column(BigInteger, ForeignKey("feed.feedid"), primary_key=True)
    productName = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    imgUrl = Column(String(255), nullable=False)
    productCategoryID = Column(BigInteger, ForeignKey("productcategory.productCategoryID"), nullable=False)
    
    # 관계 정의
    feed = relationship("Feed", back_populates="product_feed")
    category = relationship("ProductCategory", back_populates="product_feeds")
