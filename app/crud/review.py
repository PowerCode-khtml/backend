"""
리뷰 CRUD 작업
"""
from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate

def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.reviewid == review_id).first()

def get_reviews_by_feed(db: Session, feed_id: int, skip: int = 0, limit: int = 100):
    return db.query(Review).filter(Review.feedid == feed_id).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()

def get_reviews_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Review).filter(Review.userid == user_id).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(
        userid=review.userid,
        feedid=review.feedid,
        content=review.content,
        imgUrl=review.imgUrl,
        rating=review.rating
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_average_rating_by_feed(db: Session, feed_id: int):
    """피드의 평균 평점 조회"""
    from sqlalchemy import func
    result = db.query(func.avg(Review.rating)).filter(Review.feedid == feed_id).scalar()
    return float(result) if result else 0.0
