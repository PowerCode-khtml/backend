"""
피드 라우터 (해커톤 핵심 기능)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.feed import FeedCreate, FeedResponse
from app.schemas.review import ReviewCreate, ReviewResponse
from app.schemas.interaction import FeedLikeCreate
from app.crud import feed as feed_crud, review as review_crud

router = APIRouter(prefix="/feeds", tags=["feeds"])

# 피드 목록 조회 (최신순)
@router.get("/", response_model=List[FeedResponse])
def get_feeds(
    skip: int = 0, 
    limit: int = 50,
    promo_kind: str = Query(None, description="피드 타입: store, product, event"),
    db: Session = Depends(get_db)
):
    """피드 목록 조회 (해커톤 메인 화면)"""
    if promo_kind:
        return feed_crud.get_feeds_by_type(db, promo_kind=promo_kind, skip=skip, limit=limit)
    else:
        return feed_crud.get_feeds(db, skip=skip, limit=limit)

# 특정 피드 조회
@router.get("/{feed_id}", response_model=FeedResponse)
def get_feed(feed_id: int, db: Session = Depends(get_db)):
    """특정 피드 상세 조회"""
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    return feed

# 상점별 피드 조회
@router.get("/stores/{store_id}", response_model=List[FeedResponse])
def get_feeds_by_store(
    store_id: int, 
    skip: int = 0, 
    limit: int = 50, 
    db: Session = Depends(get_db)
):
    """특정 상점의 피드 목록"""
    return feed_crud.get_feeds_by_store(db, store_id=store_id, skip=skip, limit=limit)

# 피드 생성 (기본)
@router.post("/", response_model=FeedResponse)
def create_feed(feed: FeedCreate, db: Session = Depends(get_db)):
    """새 피드 생성"""
    return feed_crud.create_feed(db=db, feed=feed)

# 피드 좋아요 토글
@router.post("/{feed_id}/like")
def toggle_feed_like(
    feed_id: int,
    user_id: int,  # 해커톤용 단순화 (실제로는 JWT에서 추출)
    db: Session = Depends(get_db)
):
    """피드 좋아요/좋아요 취소"""
    # 피드 존재 확인
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    
    is_liked = feed_crud.toggle_feed_like(db, user_id=user_id, feed_id=feed_id)
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    
    return {
        "success": True,
        "is_liked": is_liked,
        "likes_count": likes_count
    }

# 피드 좋아요 수 조회
@router.get("/{feed_id}/likes")
def get_feed_likes(feed_id: int, db: Session = Depends(get_db)):
    """피드 좋아요 수 조회"""
    likes_count = feed_crud.get_feed_likes_count(db, feed_id=feed_id)
    return {"feed_id": feed_id, "likes_count": likes_count}

# 피드 리뷰 작성
@router.post("/{feed_id}/reviews", response_model=ReviewResponse)
def create_feed_review(
    feed_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """피드에 리뷰 작성"""
    # 피드 존재 확인
    feed = feed_crud.get_feed(db, feed_id=feed_id)
    if not feed:
        raise HTTPException(status_code=404, detail="피드를 찾을 수 없습니다")
    
    # 리뷰의 feedid 설정
    review.feedid = feed_id
    return review_crud.create_review(db=db, review=review)

# 피드 리뷰 목록 조회
@router.get("/{feed_id}/reviews", response_model=List[ReviewResponse])
def get_feed_reviews(
    feed_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """피드의 리뷰 목록 조회"""
    return review_crud.get_reviews_by_feed(db, feed_id=feed_id, skip=skip, limit=limit)
