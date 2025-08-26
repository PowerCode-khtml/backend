"""
상점 카테고리 모델
"""
from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.database import Base

class StoreCategory(Base):
    __tablename__ = "storecategory"
    
    storeCategoryid = Column(BigInteger, primary_key=True, autoincrement=True)
    categoryName = Column(String(30), nullable=False)
    
    # 관계 정의
    stores = relationship("Store", back_populates="category")
