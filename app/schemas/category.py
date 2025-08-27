"""
카테고리 스키마
"""
from pydantic import BaseModel
from typing import Optional

class StoreCategoryBase(BaseModel):
    categoryName: str

class StoreCategoryCreate(StoreCategoryBase):
    pass

class StoreCategoryResponse(StoreCategoryBase):
    storeCategoryid: int
    
    class Config:
        from_attributes = True

class ProductCategoryBase(BaseModel):
    categoryName: str

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategoryResponse(ProductCategoryBase):
    productCategoryID: int
    
    class Config:
        from_attributes = True

class MarketBase(BaseModel):
    marketName: str
    address: str

class MarketCreate(MarketBase):
    pass

class MarketResponse(MarketBase):
    marketid: int
    
    class Config:
        from_attributes = True
