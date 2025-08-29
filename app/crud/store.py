"""
상점 CRUD 작업 (해커톤 핵심)
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.store import Store
from app.models.subscription import Subscription
from app.models.feed import Feed
from app.models.feed_like import FeedLike
from app.models.user import User
from app.models.store_feed import StoreFeed
from app.models.product_feed import ProductFeed
from app.models.event_feed import EventFeed
from app.schemas.store import StoreCreate, StoreUpdate

def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.storeid == store_id).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()

def get_stores_by_host(db: Session, host_id: int):
    return db.query(Store).filter(Store.hostid == host_id).all()

def get_stores_by_market(db: Session, market_id: int):
    return db.query(Store).filter(Store.marketid == market_id).all()

def get_stores_by_category(db: Session, category_id: int):
    return db.query(Store).filter(Store.categoryid == category_id).all()

def create_store(db: Session, store: StoreCreate):
    db_store = Store(
        marketid=store.marketid,
        categoryid=store.categoryid,
        hostid=store.hostid,
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

def get_store_profile(db: Session, store_id: int, host_id: int):
    store = db.query(Store).filter(Store.storeid == store_id).first()
    if not store:
        return None

    follower_count = db.query(func.count(Subscription.userid)).filter(Subscription.storeid == store_id).scalar()

    total_liked_count = db.query(func.count(FeedLike.userid)).join(Feed).filter(Feed.storeid == store_id).scalar()

    is_my_store = (store.hostid == host_id)

    feeds_query = db.query(
        Feed.mediaUrl,
        func.coalesce(
            StoreFeed.description,
            ProductFeed.productName,
            EventFeed.eventName
        ).label("feedName"),
        func.count(FeedLike.userid).label("like_count"),
        Feed.promoKind.label("feedType")
    ).outerjoin(StoreFeed, Feed.feedid == StoreFeed.feedid)\
    .outerjoin(ProductFeed, Feed.feedid == ProductFeed.feedid)\
    .outerjoin(EventFeed, Feed.feedid == EventFeed.feedid)\
    .outerjoin(FeedLike, Feed.feedid == FeedLike.feedid)\
    .filter(Feed.storeid == store_id)\
    .group_by(Feed.feedid, StoreFeed.description, ProductFeed.productName, EventFeed.eventName)\
    .all()

    feeds = [
        {
            "mediaUrl": feed.mediaUrl,
            "feedName": feed.feedName,
            "like_count": feed.like_count,
            "feedType": feed.feedType.name if feed.feedType else None
        } for feed in feeds_query
    ]

    return {
        "storeImg": None,
        "followerCount": follower_count,
        "totalLikedCount": total_liked_count,
        "isMyStore": is_my_store,
        "storeDescript": store.description,
        "storeAddress": store.address,
        "storePhoneNumber": store.tel,
        "weekdayStart": store.dayOpenTime.strftime("%H:%M") if store.dayOpenTime else None,
        "weekdayEnd": store.dayCloseTime.strftime("%H:%M") if store.dayCloseTime else None,
        "weekendStart": store.weekendOpenTime.strftime("%H:%M") if store.weekendOpenTime else None,
        "weekendEnd": store.weekendCloseTime.strftime("%H:%M") if store.weekendCloseTime else None,
        "feeds": feeds
    }
