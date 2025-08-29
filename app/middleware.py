import logging
import sys
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# 로거 설정
def setup_logger():
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)
    
    # 핸들러 생성 (파일, 콘솔)
    file_handler = logging.FileHandler("api.log", encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 포매터 생성 및 핸들러에 추가
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 로거에 핸들러 추가 (중복 추가 방지)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()

        # 요청 본문 읽기
        req_body = await request.body()

        # 요청 정보와 본문 로그
        logger.info(f"REQUEST: {request.method} {request.url.path} | Client: {request.client.host} | Body: {req_body.decode('utf-8', errors='ignore')}")

        # 읽은 본문을 다시 사용 가능하도록 새로운 receive 채널 생성
        async def receive():
            return {"type": "http.request", "body": req_body}

        # 새로운 receive 채널로 요청 객체 재생성
        new_request = Request(request.scope, receive)

        response = await call_next(new_request)

        process_time = time.time() - start_time
        
        # 응답 본문을 읽기 위해 비동기적으로 순회
        res_body = b""
        async for chunk in response.body_iterator:
            res_body += chunk
        
        # 응답 정보 로그
        logger.info(f"RESPONSE: Status={response.status_code} | Took={process_time:.4f}s | Body='{res_body.decode('utf-8', errors='ignore')}'")
        
        # body_iterator가 소비되었으므로, 새로운 응답 객체를 생성하여 반환
        return Response(content=res_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type)
