"""
인증 라우터 (로그인, 회원가입)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import TypeVar, Generic, List

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.host import HostCreate, HostLogin, HostResponse
from app.schemas.auth import Token
from app.schemas.base_response import GenericResponse
from app.crud import user as user_crud, host as host_crud
from app.services.auth import AuthService

router = APIRouter(prefix="/user", tags=["authentication"])

# 사용자 회원가입
@router.post("/register", response_model=GenericResponse[UserResponse])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """사용자 회원가입"""
    # 이메일 중복 체크
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        return GenericResponse.error_response(
            error_message="이미 등록된 이메일입니다",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    created_user = user_crud.create_user(db=db, user=user)
    return GenericResponse.success_response(created_user)

# 사용자 로그인
@router.post("/login", response_model=GenericResponse[Token])
def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
    """사용자 로그인"""
    user = user_crud.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        return GenericResponse.error_response(
            error_message="이메일 또는 비밀번호가 잘못되었습니다",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    access_token = AuthService.create_access_token(
        data={"sub": user.email, "user_type": "user", "user_id": user.userid}
    )
    
    token_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "user_type": "user",
        "user_id": user.userid
    }
    return GenericResponse.success_response(Token(**token_data))

# 호스트 회원가입
@router.post("/hosts/register", response_model=GenericResponse[HostResponse])
def register_host(host: HostCreate, db: Session = Depends(get_db)):
    """호스트 회원가입"""
    # 이메일 중복 체크
    db_host = host_crud.get_host_by_email(db, email=host.email)
    if db_host:
        return GenericResponse.error_response(
            error_message="이미 등록된 이메일입니다",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    created_host = host_crud.create_host(db=db, host=host)
    return GenericResponse.success_response(created_host)

# 호스트 로그인
@router.post("/hosts/login", response_model=GenericResponse[Token])
def login_host(host_login: HostLogin, db: Session = Depends(get_db)):
    """호스트 로그인"""
    host = host_crud.authenticate_host(db, host_login.email, host_login.password)
    if not host:
        return GenericResponse.error_response(
            error_message="이메일 또는 비밀번호가 잘못되었습니다",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    access_token = AuthService.create_access_token(
        data={"sub": host.email, "user_type": "host", "user_id": host.hostID}
    )
    
    token_data = {
        "access_token": access_token,
        "token_type": "bearer", 
        "user_type": "host",
        "user_id": host.hostID
    }
    return GenericResponse.success_response(Token(**token_data))
