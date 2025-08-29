"""
인증 라우터 (로그인, 회원가입)
"""
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import Union, Optional

from app.crud import user as user_crud, host as host_crud
from app.database import get_db
from app.schemas.auth import Token
from app.schemas.base_response import GenericResponse
from app.schemas.host import HostCreate, HostLogin, HostResponse
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/user", tags=["authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    isHost: bool


class HostLoginResponse(BaseModel):
    hostId: int


@router.post("/register", response_model=GenericResponse[Union[UserResponse, HostResponse]])
def register(request_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    사용자 및 호스트 회원가입

    - **isHost** (boolean): `true`이면 호스트로, `false`이면 일반 사용자로 가입합니다.
    """
    if request_data.isHost:
        # 호스트 회원가입
        db_host = host_crud.get_host_by_email(db, email=request_data.email)
        if db_host:
            return GenericResponse.error_response(
                error_message="이미 등록된 이메일입니다",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        host_create = HostCreate(
            email=request_data.email,
            password=request_data.password,
            name=request_data.name,
        )
        created_host = host_crud.create_host(db=db, host=host_create)
        return GenericResponse.success_response(created_host)
    else:
        # 사용자 회원가입
        db_user = user_crud.get_user_by_email(db, email=request_data.email)
        if db_user:
            return GenericResponse.error_response(
                error_message="이미 등록된 이메일입니다",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user_create = UserCreate(
            email=request_data.email,
            password=request_data.password,
            name=request_data.name
        )
        created_user = user_crud.create_user(db=db, user=user_create)
        return GenericResponse.success_response(created_user)


# # 사용자 로그인
# @router.post("/login", response_model=GenericResponse[Token])
# def login_user(user_login: UserLogin, db: Session = Depends(get_db)):
#     """사용자 로그인"""
#     user = user_crud.authenticate_user(db, user_login.email, user_login.password)
#     if not user:
#         return GenericResponse.error_response(
#             error_message="이메일 또는 비밀번호가 잘못되었습니다",
#             status_code=status.HTTP_401_UNAUTHORIZED
#         )

#     access_token = AuthService.create_access_token(
#         data={"sub": user.email, "userType": "user", "userId": user.userid}
#     )

#     token_data = {
#         "accessToken": access_token,
#         "tokenType": "bearer",
#         "userType": "user",
#         "userId": user.userid
#     }
#     return GenericResponse.success_response(Token(**token_data))


# 호스트 로그인
@router.post("/login", response_model=GenericResponse[HostLoginResponse])
def login_host(host_login: HostLogin, db: Session = Depends(get_db)):
    """호스트 로그인"""
    host = host_crud.authenticate_host(db, host_login.email, host_login.password)
    if not host:
        return GenericResponse.error_response(
            error_message="이메일 또는 비밀번호가 잘못되었습니다",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return GenericResponse.success_response(HostLoginResponse(hostId=host.hostid))