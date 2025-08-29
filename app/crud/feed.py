"""
피드 CRUD 작업 (해커톤 핵심 기능)
"""
from sqlalchemy.orm import Session
from app.models.feed import Feed
from app.models.store import Store
from app.models.store_feed import StoreFeed
from app.models.product_feed import ProductFeed
from app.models.event_feed import EventFeed
from app.models.feed_like import FeedLike
from app.models.review import Review # Add this import for review count
from sqlalchemy import text # Add this import
import datetime

def get_feed(db: Session, feed_id: int):
    return db.query(Feed).filter(Feed.feedid == feed_id).first()

def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Feed).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_by_store(db: Session, store_id: int, skip: int = 0, limit: int = 50):
    return db.query(Feed).filter(Feed.storeid == store_id).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_by_type(db: Session, promo_kind: str, skip: int = 0, limit: int = 50):
    return db.query(Feed).filter(Feed.promoKind == promo_kind).order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_by_market(db: Session, market_id: int, promo_kind: str = None, skip: int = 0, limit: int = 50):
    """
    특정 시장에 속한 모든 상점의 피드를 가져옵니다.
    """
    # 1. market_id에 해당하는 store_id 목록을 가져옵니다.
    store_ids = db.query(Store.storeid).filter(Store.marketid == market_id).all()
    store_ids = [s[0] for s in store_ids]

    if not store_ids:
        return []

    # 2. 해당 store_id 목록에 포함되는 피드를 조회합니다.
    query = db.query(Feed).filter(Feed.storeid.in_(store_ids))

    if promo_kind:
        query = query.filter(Feed.promoKind == promo_kind)

    return query.order_by(Feed.created_at.desc()).offset(skip).limit(limit).all()

def get_feeds_details_by_market(db: Session, market_id: int, user_id: int, skip: int = 0, limit: int = 50):
    sql_query = text(f"""
    SELECT
        f.feedid AS feedId,
        s.storeName AS storeName,
        h.imgUrl AS storeImageUrl,
        f.created_at AS createdAt,
        f.body AS feedContent,
        f.mediaUrl AS feedImageUrl,
        f.promoKind AS feedType,
        COUNT(DISTINCT fl.userid) AS feedLikeCount,
        COUNT(DISTINCT r.reviewid) AS feedReviewCount,
        CASE WHEN EXISTS (
            SELECT 1
            FROM feedlike fl_user
            WHERE fl_user.feedid = f.feedid AND fl_user.userid = :user_id
        ) THEN TRUE ELSE FALSE END AS isLiked
    FROM feed f
    JOIN store s ON f.storeid = s.storeid
    JOIN host h ON s.hostid = h.hostid
    LEFT JOIN feedlike fl ON f.feedid = fl.feedid
    LEFT JOIN review r ON f.feedid = r.feedid
    WHERE s.marketid = :market_id
    GROUP BY f.feedid, s.storeName, h.imgUrl, f.created_at, f.body, f.mediaUrl, f.promoKind
    ORDER BY f.created_at DESC
    LIMIT :limit OFFSET :offset;
    """)
    
    result = db.execute(sql_query, {"market_id": market_id, "user_id": user_id, "limit": limit, "offset": skip}).mappings().all()
    return result

def create_feed_with_details(
    db: Session,
    feed_type: str,
    media_type: str,
    store_id: int,
    feed_body: str,
    feed_media_url: str,
    # Store-specific
    store_description: str = None,
    store_image_url: str = None,
    # Product-specific
    product_name: str = None,
    category_id: int = None,
    product_description: str = None,
    product_image_url: str = None,
    # Event-specific
    event_name: str = None,
    event_description: str = None,
    event_start_at: datetime.datetime = None,
    event_end_at: datetime.datetime = None,
    event_image_url: str = None,
):
    """
    피드와 세부 정보를 한 번에 생성합니다.
    """
    # 1. 기본 피드 생성
    db_feed = Feed(
        storeid=store_id,
        promoKind=feed_type,
        mediaType=media_type,
        mediaUrl=feed_media_url,
        body=feed_body,
        prompt=""
    )
    db.add(db_feed)
    db.flush()

    # 2. 피드 타입에 따라 세부 정보 생성
    if feed_type == "store":
        db_store_feed = StoreFeed(
            feedid=db_feed.feedid,
            description=store_description,
            imgUrl=store_image_url
        )
        db.add(db_store_feed)
    elif feed_type == "product":
        db_product_feed = ProductFeed(
            feedid=db_feed.feedid,
            productName=product_name,
            description=product_description,
            imgUrl=product_image_url,
            productCategoryID=category_id
        )
        db.add(db_product_feed)
    elif feed_type == "event":
        db_event_feed = EventFeed(
            feedid=db_feed.feedid,
            eventName=event_name,
            description=event_description,
            imgUrl=event_image_url,
            start_at=event_start_at,
            end_at=event_end_at
        )
        db.add(db_event_feed)

    db.commit()
    db.refresh(db_feed)
    return db_feed

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
