"""
상품 카테고리 모델
"""
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.database import Base

class ProductCategory(Base):
    __tablename__ = "productcategory"
    
    productCategoryid = Column(BigInteger, primary_key=True, autoincrement=True)
    productCategoryName = Column(String(50), nullable=False)
    
    # 관계 정의
    product_feeds = relationship("ProductFeed", back_populates="category")
