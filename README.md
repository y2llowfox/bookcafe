# BookCafe - 북카페 관리 시스템

Flask 기반의 북카페 통합 관리 웹 애플리케이션입니다. 회원 관리, 도서 대출/반납, 매출 관리, 통계 대시보드를 제공하며, PWA를 지원하여 모바일에서도 앱처럼 사용할 수 있습니다.

## 주요 기능

- **회원 관리** — 등록, 검색, 수정, 비활성화 / 등급 시스템 (BASIC → SILVER → GOLD → VIP)
- **도서 관리** — 도서 등록, 카테고리별 검색, 재고 관리
- **대출/반납** — 도서 대출 및 반납 처리, 연체 관리 (대출 기간 14일)
- **매출 관리** — 매출 등록, 포인트 적립(5%) 및 사용
- **통계 대시보드** — 일/월별 매출, 회원 등급 분포, 인기 도서 TOP 10, 월별 매출 추이
- **PWA 지원** — 모바일 하단 탭바, Service Worker, 홈 화면에 추가 가능

## 회원 등급 시스템

| 등급 | 조건 (누적 포인트) |
|------|-------------------|
| BASIC | 0P ~ |
| SILVER | 1,000P ~ |
| GOLD | 3,000P ~ |
| VIP | 5,000P ~ |

매출 시 결제 금액의 5%가 포인트로 적립되며, 적립된 포인트는 결제 시 사용 가능합니다.

## 프로젝트 구조

```
bookcafe/
├── app.py                  # Flask 앱 진입점
├── models.py               # DB 모델 (Member, Book, Rental, Sale)
├── routes/
│   ├── members.py          # 회원 관리 라우트
│   ├── books.py            # 도서 관리 + 대출/반납 라우트
│   ├── sales.py            # 매출 관리 라우트
│   └── stats.py            # 통계 대시보드 라우트
├── templates/
│   ├── base.html           # 기본 레이아웃 (네비게이션 + 모바일 탭바)
│   ├── index.html          # 메인 대시보드
│   ├── members/            # 회원 관련 템플릿
│   ├── books/              # 도서 관련 템플릿
│   ├── sales/              # 매출 관련 템플릿
│   └── stats/              # 통계 관련 템플릿
├── static/
│   ├── style.css           # 커스텀 스타일
│   ├── manifest.json       # PWA 매니페스트
│   ├── sw.js               # Service Worker
│   └── icon.svg            # 앱 아이콘
├── bookcafe.db             # SQLite 데이터베이스
└── requirements.txt
```

## 설치 및 실행

```bash
git clone https://github.com/y2llowfox/bookcafe.git
cd bookcafe
pip install -r requirements.txt
python app.py
```

브라우저에서 `http://localhost:5000` 접속

## 기술 스택

| 분류 | 기술 |
|------|------|
| 백엔드 | Flask, Flask-SQLAlchemy |
| 데이터베이스 | SQLite |
| 프론트엔드 | Bootstrap 5, Bootstrap Icons |
| PWA | Service Worker, Web App Manifest |

## 라이선스

MIT License
