"""
피드 CRUD 작업 (해커톤 핵심 기능)
"""
from sqlalchemy.orm import Session
from app.models.feed import Feed
from app.models.store_feed import StoreFeed
from app.models.product_feed import ProductFeed
from app.models.event_feed import EventFeed
from app.models.feed_like import FeedLike
from app.schemas.feed import FeedCreate

def get_feed(db: Session, feed_id: int):
    return db.query(Feed).filter(Feed.feedid == feed_id).first()

def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Feed).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_by_store(db: Session, store_id: int, skip: int = 0, limit: int = 50):
    return db.query(Feed).filter(Feed.storeid == store_id).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_by_type(db: Session, promo_kind: str, skip: int = 0, limit: int = 50):
    return db.query(Feed).filter(Feed.promoKind == promo_kind).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def create_feed(db: Session, feed: FeedCreate):
    """기본 피드 생성"""
    db_feed = Feed(
        storeid=feed.storeid,
        promoKind=feed.promoKind,
        mediaType=feed.mediaType,
        prompt=feed.prompt,
        mediaUrl=feed.mediaUrl,
        body=feed.body
    )
    db.add(db_feed)
    db.commit()
    db.refresh(db_feed)
    return db_feed

def create_store_feed_detail(db: Session, feed_id: int, description: str = None, imgUrl: str = ""):
    """상점 피드 상세 정보 생성"""
    db_store_feed = StoreFeed(
        feedid=feed_id,
        description=description,
        imgUrl=imgUrl
    )
    db.add(db_store_feed)
    db.commit()
    db.refresh(db_store_feed)
    return db_store_feed

def create_product_feed_detail(db: Session, feed_id: int, product_name: str, 
                             description: str, imgUrl: str, category_id: int):
    """상품 피드 상세 정보 생성"""
    db_product_feed = ProductFeed(
        feedid=feed_id,
        productName=product_name,
        description=description,
        imgUrl=imgUrl,
        productCategoryID=category_id
    )
    db.add(db_product_feed)
    db.commit()
    db.refresh(db_product_feed)
    return db_product_feed

def create_event_feed_detail(db: Session, feed_id: int, event_name: str,
                           description: str, imgUrl: str, start_at, end_at):
    """이벤트 피드 상세 정보 생성"""
    db_event_feed = EventFeed(
        feedid=feed_id,
        eventName=event_name,
        description=description,
        imgUrl=imgUrl,
        start_at=start_at,
        end_at=end_at
    )
    db.add(db_event_feed)
    db.commit()
    db.refresh(db_event_feed)
    return db_event_feed

def toggle_feed_like(db: Session, user_id: int, feed_id: int):
    """피드 좋아요 토글"""
    existing_like = db.query(FeedLike).filter(
        FeedLike.userid == user_id,
        FeedLike.feedid == feed_id
    ).first()
    
    if existing_like:
        # 좋아요 취소
        db.delete(existing_like)
        db.commit()
        return False  # 좋아요 취소됨
    else:
        # 좋아요 추가
        new_like = FeedLike(userid=user_id, feedid=feed_id)
        db.add(new_like)
        db.commit()
        return True  # 좋아요 추가됨

def get_feed_likes_count(db: Session, feed_id: int):
    """피드 좋아요 수 조회"""
    return db.query(FeedLike).filter(FeedLike.feedid == feed_id).count()
