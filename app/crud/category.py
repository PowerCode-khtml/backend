"""
카테고리 CRUD 작업
"""
from sqlalchemy.orm import Session
from app.models.market import Market
from app.models.store_category import StoreCategory
from app.models.product_category import ProductCategory
from app.schemas.category import MarketCreate, StoreCategoryCreate, ProductCategoryCreate

# Market CRUD
def get_market(db: Session, market_id: int):
    return db.query(Market).filter(Market.marketid == market_id).first()

def get_markets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Market).offset(skip).limit(limit).all()

def create_market(db: Session, market: MarketCreate):
    db_market = Market(
        marketName=market.marketName,
        address=market.address
    )
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market

# Store Category CRUD
def get_store_category(db: Session, category_id: int):
    return db.query(StoreCategory).filter(StoreCategory.storeCategoryid == category_id).first()

def get_store_categories(db: Session):
    return db.query(StoreCategory).all()

def create_store_category(db: Session, category: StoreCategoryCreate):
    db_category = StoreCategory(categoryName=category.categoryName)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# Product Category CRUD
def get_product_category(db: Session, category_id: int):
    return db.query(ProductCategory).filter(ProductCategory.productCategoryID == category_id).first()

def get_product_categories(db: Session):
    return db.query(ProductCategory).all()

def create_product_category(db: Session, category: ProductCategoryCreate):
    db_category = ProductCategory(categoryName=category.categoryName)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
