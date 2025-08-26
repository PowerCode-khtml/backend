# 🎉 해커톤 마켓플레이스 + AI 이미지 생성 API

해커톤용 피드 기반 마켓플레이스 백엔드 API + OpenAI 이미지 생성 기능

## 🎯 해커톤 핵심 기능

### **📱 피드 시스템** (메인 기능)
- **통합 피드**: 상점/상품/이벤트 피드 통합 관리
- **실시간 좋아요**: 사용자 상호작용
- **리뷰 시스템**: 피드별 리뷰 및 평점

### **🤖 AI 이미지 생성** (특별 기능)
- **OpenAI DALL-E 3** 활용
- **빠른 포스터 생성**: 상점 정보 기반
- **자동 피드 등록**: 생성된 이미지 자동 피드화

### **🔐 사용자 인증**
- **이중 인증**: 일반 사용자 + 호스트
- **JWT 토큰**: 간단하고 안전한 인증

## 🚀 빠른 시작

### **1. 환경 설정**
```bash
# 프로젝트 클론
git clone [repository]
cd hackathon-fastapi

# 환경 변수 설정
cp .env.example .env
# .env 파일 편집:
# - DATABASE_URL: RDS 등 외부 DB URL
# - OPENAI_API_KEY: OpenAI API 키
```

### **2. 의존성 설치**
```bash
pip install -r requirements.txt
```

### **3. 서버 실행**
```bash
# 방법 1: 스크립트 사용 (권장)
./start.sh

# 방법 2: 직접 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### **4. 접속 확인**
- **🌐 메인**: http://localhost:8000
- **📚 API 문서**: http://localhost:8000/docs
- **🎯 해커톤 정보**: http://localhost:8000/hackathon

## 📊 데이터베이스 구조

### **핵심 테이블**
```
user          - 사용자 정보
host          - 호스트 정보  
store         - 상점 정보
feed          - 통합 피드 시스템 ⭐
feedlike      - 피드 좋아요
subscription  - 상점 구독
review        - 리뷰 시스템
```

### **피드 시스템** (핵심)
```
feed 테이블:
- promoKind: "store" | "product" | "event"
- mediaType: "image" | "video" 
- prompt: AI 이미지 생성용 프롬프트
- mediaUrl: 생성된 미디어 URL
- body: 피드 내용
```

## 🛠️ API 엔드포인트

### **🔑 인증 (`/api/auth`)**
```bash
POST /api/auth/users/register    # 사용자 회원가입
POST /api/auth/users/login       # 사용자 로그인
POST /api/auth/hosts/register    # 호스트 회원가입  
POST /api/auth/hosts/login       # 호스트 로그인
```

### **📱 피드 (`/api/feeds`)** ⭐ 핵심
```bash
GET  /api/feeds/                 # 피드 목록 (최신순)
GET  /api/feeds/{feed_id}        # 특정 피드 조회
GET  /api/feeds/stores/{store_id} # 상점별 피드
POST /api/feeds/                 # 새 피드 생성
POST /api/feeds/{feed_id}/like   # 좋아요 토글
GET  /api/feeds/{feed_id}/likes  # 좋아요 수 조회
POST /api/feeds/{feed_id}/reviews # 리뷰 작성
GET  /api/feeds/{feed_id}/reviews # 리뷰 목록
```

### **🤖 AI 이미지 (`/api/images`)** ⭐ 특별 기능
```bash
POST /api/images/quick-poster    # 빠른 포스터 생성
POST /api/images/generate        # 고급 이미지 생성
GET  /api/images/download/{filename} # 이미지 다운로드
```

### **🏪 상점 (`/api/stores`)**
```bash
GET  /api/stores/                # 상점 목록
GET  /api/stores/{store_id}      # 특정 상점
POST /api/stores/                # 상점 생성
PUT  /api/stores/{store_id}      # 상점 수정
```

## 💻 사용 예시

### **1. 사용자 회원가입 & 로그인**
```python
import requests

# 회원가입
user_data = {
    "email": "hackathon@example.com",
    "name": "해커톤 참가자",
    "password": "hackathon2024"
}
response = requests.post("http://localhost:8000/api/auth/users/register", json=user_data)

# 로그인
login_data = {"email": "hackathon@example.com", "password": "hackathon2024"}
response = requests.post("http://localhost:8000/api/auth/users/login", json=login_data)
token = response.json()["access_token"]
```

### **2. AI 포스터 생성** (해커톤 특별 기능)
```python
# 빠른 포스터 생성
poster_data = {
    "storeid": 1,
    "message": "해커톤 특별 할인 이벤트!",
    "style": "modern"
}

response = requests.post("http://localhost:8000/api/images/quick-poster", json=poster_data)
result = response.json()

if result["success"]:
    print(f"생성된 피드 ID: {result['feedid']}")
    print(f"이미지 URL: {result['mediaUrl']}")
```

### **3. 피드 조회 및 좋아요**
```python
# 피드 목록 조회
response = requests.get("http://localhost:8000/api/feeds/")
feeds = response.json()

# 첫 번째 피드에 좋아요
if feeds:
    feed_id = feeds[0]["feedid"]
    like_data = {"user_id": 1}  # 실제로는 JWT에서 추출
    requests.post(f"http://localhost:8000/api/feeds/{feed_id}/like", params={"user_id": 1})
```

### **4. 리뷰 작성**
```python
# 피드에 리뷰 작성
review_data = {
    "content": "해커톤에서 만든 AI 포스터가 정말 멋져요!",
    "rating": 5,
    "userid": 1
}

response = requests.post(f"http://localhost:8000/api/feeds/{feed_id}/reviews", json=review_data)
```

## 🧪 테스트

### **자동 테스트 실행**
```bash
# API 테스트 스크립트
python test_api.py
```

**테스트 항목:**
- ✅ 헬스체크
- ✅ 사용자 인증
- ✅ 피드 시스템
- ✅ AI 이미지 생성

## ⚙️ 환경 변수

**.env 파일 설정:**
```env
# 데이터베이스 (RDS 등 외부 DB)
DATABASE_URL=mysql+pymysql://user:pass@host:port/db_name

# OpenAI API 키 (필수!)
OPENAI_API_KEY=your_openai_api_key_here

# JWT 시크릿
SECRET_KEY=your-hackathon-secret-key

# 서버 설정
DEBUG=true
HOST=0.0.0.0
PORT=8000
```

## 📈 해커톤 활용 시나리오

### **시나리오 1: 실시간 마켓플레이스**
1. **호스트** 상점 등록
2. **AI**로 매력적인 포스터 생성
3. **피드**에 자동 등록
4. **사용자들** 좋아요 & 리뷰

### **시나리오 2: 이벤트 마케팅**
1. **특별 할인** 이벤트 기획
2. **AI 포스터** 생성 (`quick-poster`)
3. **소셜 피드**로 확산
4. **실시간 반응** 확인

### **시나리오 3: 사용자 참여**
1. **피드 둘러보기** (최신순)
2. **관심 상점** 구독
3. **리뷰 작성** & 평점
4. **좋아요**로 상호작용

## 🎨 AI 이미지 생성 기능

### **빠른 포스터 생성**
```python
# 상점 정보만으로 간편하게
{
    "storeid": 1,
    "message": "새로운 메뉴 출시!",
    "style": "modern"
}
```

### **고급 이미지 생성**
```python
# 상품/이벤트별 맞춤 생성
{
    "storeid": 1,
    "promoKind": "product",
    "productName": "해커톤 버거",
    "productDescription": "개발자들을 위한 특별한 버거"
}
```

## 🏗️ 프로젝트 구조

```
hackathon-fastapi/
├── app/
│   ├── models/          # 데이터베이스 모델 (16개)
│   ├── schemas/         # API 스키마 (10개)  
│   ├── crud/           # CRUD 작업 (6개)
│   ├── routers/        # API 라우터 (5개)
│   ├── services/       # 비즈니스 로직 (2개)
│   ├── database.py     # DB 연결
│   └── main.py         # FastAPI 앱
├── generated/          # AI 생성 이미지 저장
├── uploads/            # 업로드 파일 저장
├── requirements.txt    # Python 패키지
├── .env.example       # 환경 변수 템플릿
├── start.sh           # 실행 스크립트
├── test_api.py        # API 테스트
├── init_db.sql        # DB 초기화
└── README.md          # 프로젝트 문서
```

## 🚨 해커톤 주의사항

### **필수 설정**
1. **OpenAI API 키** 반드시 설정 (이미지 생성용)
2. **외부 데이터베이스** URL 설정 (RDS 등)
3. **CORS 설정** - 현재 모든 오리진 허용 (해커톤용)

### **성능 최적화**
- **피드 조회**: 최신순 정렬, 페이징 지원
- **이미지 캐싱**: 생성된 이미지 재사용
- **데이터베이스**: 외래키 및 인덱스 최적화

### **보안 참고**
- JWT 토큰 유효시간: 24시간 (해커톤용 길게 설정)
- 비밀번호 해싱: bcrypt 사용
- CORS: 프로덕션 시 제한 필요

## 🏆 해커톤 우승 전략

### **차별화 포인트**
1. **🤖 AI 이미지 생성** - OpenAI 활용한 자동 마케팅
2. **📱 피드 시스템** - 소셜 미디어 스타일
3. **⚡ 실시간 상호작용** - 좋아요, 리뷰, 구독
4. **🎯 사용자 친화적 API** - 직관적이고 빠른 개발

### **확장 가능성**
- **실시간 알림** 시스템
- **추천 알고리즘** (AI 기반)
- **소셜 로그인** 연동
- **결제 시스템** 통합

---

**🎉 해커톤 화이팅! 멋진 서비스를 만들어보세요!**

## 📞 지원

문제가 발생하거나 질문이 있으시면:
- **API 문서**: http://localhost:8000/docs
- **헬스체크**: http://localhost:8000/health
- **해커톤 정보**: http://localhost:8000/hackathon
