"""
사용자 라우터
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.review import ReviewResponse
from app.crud import user as user_crud, review as review_crud

router = APIRouter(prefix="/users", tags=["users"])

# 사용자 프로필 조회
@router.get("/{user_id}", response_model=UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """사용자 프로필 조회"""
    user = user_crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

# 사용자 프로필 수정
@router.put("/{user_id}", response_model=UserResponse)
def update_user_profile(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """사용자 프로필 수정"""
    user = user_crud.update_user(db, user_id=user_id, user_update=user_update)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

# 사용자 리뷰 목록
@router.get("/{user_id}/reviews", response_model=List[ReviewResponse])
def get_user_reviews(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """사용자가 작성한 리뷰 목록"""
    return review_crud.get_reviews_by_user(db, user_id=user_id, skip=skip, limit=limit)
