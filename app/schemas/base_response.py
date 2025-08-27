from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

# T는 responseDto의 타입을 나타내는 타입 변수입니다.
T = TypeVar('T')

class MessageResponse(BaseModel):
    message: str

class GenericResponse(BaseModel, Generic[T]):
    responseDto: Optional[T] = None
    error: Optional[str] = None
    success: bool = True

    # 성공 응답을 위한 헬퍼 메서드
    @classmethod
    def success_response(cls, data: T):
        return cls(responseDto=data, success=True, error=None)

    # 에러 응답을 위한 헬퍼 메서드
    @classmethod
    def error_response(cls, error_message: str, status_code: int = 400):
        # FastAPI의 HTTPException과 통합하기 위해 status_code를 추가했지만,
        # 실제 반환 시에는 error 필드만 사용합니다.
        return cls(responseDto=None, success=False, error=error_message)
