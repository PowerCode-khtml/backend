-- 해커톤용 데이터베이스 초기화 스크립트
-- RDS 등 외부 데이터베이스에서 실행

-- 기본 카테고리 데이터 삽입
INSERT IGNORE INTO storecategory (categoryName) VALUES 
('음식점'),
('카페'),
('마트'),
('치킨전문점'),
('패스트푸드'),
('한식'),
('일식'),
('중식'),
('양식'),
('분식');

INSERT IGNORE INTO productcategory (productCategoryName) VALUES 
('음식'),
('음료'),
('디저트'),
('세트메뉴'),
('사이드'),
('주류'),
('간식'),
('특산품');

INSERT IGNORE INTO paymentMethod (paymentMethodName) VALUES 
('현금'),
('카드'),
('제로페이'),
('카카오페이'),
('네이버페이'),
('페이코'),
('토스');

-- 샘플 마켓 데이터
INSERT IGNORE INTO market (marketName, address) VALUES 
('해커톤 마켓', '서울시 강남구 테헤란로 123'),
('스타트업 거리', '서울시 서초구 서초대로 456'),
('IT 밸리', '경기도 성남시 분당구 정자일로 789');

-- 샘플 호스트 (비밀번호는 "hackathon2024"를 해시화한 값)
INSERT IGNORE INTO host (email, name, password) VALUES 
('host1@hackathon.com', '해커톤 호스트1', '$2b$12$example_hashed_password'),
('host2@hackathon.com', '해커톤 호스트2', '$2b$12$example_hashed_password');

-- 샘플 상점
INSERT IGNORE INTO store (marketid, categoryid, hostID, storeName, tel, address, description) VALUES 
(1, 1, 1, '해커톤 맛집', '02-1234-5678', '서울시 강남구 테헤란로 123-1', '해커톤 참가자들을 위한 맛있는 음식을 제공합니다'),
(1, 2, 1, '코딩 카페', '02-2345-6789', '서울시 강남구 테헤란로 123-2', '개발자들의 성지, 24시간 운영'),
(2, 4, 2, '버그 치킨', '02-3456-7890', '서울시 서초구 서초대로 456-1', '코드의 버그를 치킨으로 달래드립니다');

-- 샘플 사용자
INSERT IGNORE INTO user (email, name, password) VALUES 
('user1@hackathon.com', '해커톤 참가자1', '$2b$12$example_hashed_password'),
('user2@hackathon.com', '해커톤 참가자2', '$2b$12$example_hashed_password');

-- 샘플 피드
INSERT IGNORE INTO feed (storeid, promoKind, mediaType, prompt, mediaUrl, body) VALUES 
(1, 'store', 'image', 'Delicious food poster', '/generated/sample_food.jpg', '해커톤 맛집의 새로운 메뉴를 소개합니다!'),
(2, 'store', 'image', 'Cozy cafe poster', '/generated/sample_cafe.jpg', '24시간 코딩을 위한 완벽한 카페입니다'),
(3, 'product', 'image', 'Fried chicken poster', '/generated/sample_chicken.jpg', '버그를 잡아먹는 치킨이 출시되었습니다!');
