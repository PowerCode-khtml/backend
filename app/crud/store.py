"""
상점 CRUD 작업 (해커톤 핵심)
"""
from sqlalchemy.orm import Session
from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate

def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.storeid == store_id).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()

def get_stores_by_host(db: Session, host_id: int):
    return db.query(Store).filter(Store.hostID == host_id).all()

def get_stores_by_market(db: Session, market_id: int):
    return db.query(Store).filter(Store.marketid == market_id).all()

def get_stores_by_category(db: Session, category_id: int):
    return db.query(Store).filter(Store.categoryid == category_id).all()

def create_store(db: Session, store: StoreCreate):
    db_store = Store(
        marketid=store.marketid,
        categoryid=store.categoryid,
        hostID=store.hostID,
        storeName=store.storeName,
        tel=store.tel,
        dayOpenTime=store.dayOpenTime,
        dayCloseTime=store.dayCloseTime,
        weekendOpenTime=store.weekendOpenTime,
        weekendCloseTime=store.weekendCloseTime,
        address=store.address,
        description=store.description
    )
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def update_store(db: Session, store_id: int, store_update: StoreUpdate):
    db_store = get_store(db, store_id)
    if db_store:
        update_data = store_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_store, field, value)
        db.commit()
        db.refresh(db_store)
    return db_store

def delete_store(db: Session, store_id: int):
    db_store = get_store(db, store_id)
    if db_store:
        db.delete(db_store)
        db.commit()
    return db_store
