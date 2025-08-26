#!/bin/bash
# 해커톤용 FastAPI 실행 스크립트

echo "🎉 해커톤 FastAPI 서버 시작"
echo ""

# 환경 변수 파일 체크
if [ ! -f .env ]; then
    echo "📝 .env 파일을 생성하세요!"
    echo "   cp .env.example .env"
    echo "   그리고 데이터베이스 URL과 OpenAI API 키를 설정하세요"
    exit 1
fi

# 의존성 설치 확인
echo "📦 의존성 설치 확인 중..."
pip install -r requirements.txt

echo ""
echo "🚀 서버 시작 중..."
echo "   - 주소: http://localhost:8000"
echo "   - API 문서: http://localhost:8000/docs"
echo "   - 해커톤 정보: http://localhost:8000/hackathon"

# uvicorn으로 서버 실행 (reload 모드)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
