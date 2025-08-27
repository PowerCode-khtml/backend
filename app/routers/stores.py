"""
상점 라우터
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.schemas.base_response import GenericResponse, MessageResponse
from app.crud import store as store_crud

router = APIRouter(prefix="/stores", tags=["stores"])

# 상점 목록 조회
@router.get("/", response_model=GenericResponse[List[StoreResponse]])
def get_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """상점 목록 조회"""
    stores = store_crud.get_stores(db, skip=skip, limit=limit)
    return GenericResponse.success_response(stores)

# 특정 상점 조회
@router.get("/{store_id}", response_model=GenericResponse[StoreResponse])
def get_store(store_id: int, db: Session = Depends(get_db)):
    """특정 상점 조회"""
    store = store_crud.get_store(db, store_id=store_id)
    if store is None:
        return GenericResponse.error_response(
            error_message="상점을 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return GenericResponse.success_response(store)

# 호스트별 상점 조회
@router.get("/hosts/{host_id}", response_model=GenericResponse[List[StoreResponse]])
def get_stores_by_host(host_id: int, db: Session = Depends(get_db)):
    """특정 호스트의 상점들"""
    stores = store_crud.get_stores_by_host(db, host_id=host_id)
    return GenericResponse.success_response(stores)

# 마켓별 상점 조회
@router.get("/markets/{market_id}", response_model=GenericResponse[List[StoreResponse]])
def get_stores_by_market(market_id: int, db: Session = Depends(get_db)):
    """특정 마켓의 상점들"""
    stores = store_crud.get_stores_by_market(db, market_id=market_id)
    return GenericResponse.success_response(stores)

# 상점 생성
@router.post("/", response_model=GenericResponse[StoreResponse])
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    """새 상점 등록"""
    created_store = store_crud.create_store(db=db, store=store)
    return GenericResponse.success_response(created_store)

# 상점 수정
@router.put("/{store_id}", response_model=GenericResponse[StoreResponse])
def update_store(
    store_id: int,
    store_update: StoreUpdate,
    db: Session = Depends(get_db)
):
    """상점 정보 수정"""
    store = store_crud.update_store(db, store_id=store_id, store_update=store_update)
    if store is None:
        return GenericResponse.error_response(
            error_message="상점을 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return GenericResponse.success_response(store)

# 상점 삭제
@router.delete("/{store_id}", response_model=GenericResponse[MessageResponse])
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """상점 삭제"""
    store = store_crud.delete_store(db, store_id=store_id)
    if store is None:
        return GenericResponse.error_response(
            error_message="상점을 찾을 수 없습니다",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return GenericResponse.success_response(MessageResponse(message="상점이 삭제되었습니다"))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.crud import store as store_crud

router = APIRouter(prefix="/stores", tags=["stores"])

# 상점 목록 조회
@router.get("/", response_model=List[StoreResponse])
def get_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """상점 목록 조회"""
    return store_crud.get_stores(db, skip=skip, limit=limit)

# 특정 상점 조회
@router.get("/{store_id}", response_model=StoreResponse)
def get_store(store_id: int, db: Session = Depends(get_db)):
    """특정 상점 조회"""
    store = store_crud.get_store(db, store_id=store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다")
    return store

# 호스트별 상점 조회
@router.get("/hosts/{host_id}", response_model=List[StoreResponse])
def get_stores_by_host(host_id: int, db: Session = Depends(get_db)):
    """특정 호스트의 상점들"""
    return store_crud.get_stores_by_host(db, host_id=host_id)

# 마켓별 상점 조회
@router.get("/markets/{market_id}", response_model=List[StoreResponse])
def get_stores_by_market(market_id: int, db: Session = Depends(get_db)):
    """특정 마켓의 상점들"""
    return store_crud.get_stores_by_market(db, market_id=market_id)

# 상점 생성
@router.post("/", response_model=StoreResponse)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):
    """새 상점 등록"""
    return store_crud.create_store(db=db, store=store)

# 상점 수정
@router.put("/{store_id}", response_model=StoreResponse)
def update_store(
    store_id: int,
    store_update: StoreUpdate,
    db: Session = Depends(get_db)
):
    """상점 정보 수정"""
    store = store_crud.update_store(db, store_id=store_id, store_update=store_update)
    if store is None:
        raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다")
    return store

# 상점 삭제
@router.delete("/{store_id}")
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """상점 삭제"""
    store = store_crud.delete_store(db, store_id=store_id)
    if store is None:
        raise HTTPException(status_code=404, detail="상점을 찾을 수 없습니다")
    return {"message": "상점이 삭제되었습니다"}
