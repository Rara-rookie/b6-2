# memo_app

FastAPI, SQLAlchemy, Jinja2로 만든 게시판형 메모 웹 서비스다.  
브라우저에서 메모를 등록하고, 목록을 보고, 상세를 확인하고, 수정하고, 삭제할 수 있다.

## 실행 환경

- Python 3.10 이상
- 사용 패키지
  - fastapi 0.137.1
  - uvicorn 0.49.0
  - sqlalchemy 2.0.53
  - jinja2 3.1.5
  - python-multipart 0.0.32

## 프로젝트 구조

```text
memo_app/
├── __init__.py
├── main.py
├── database.py
├── templates.py
├── schemas.py
├── models/
│   ├── __init__.py
│   └── memo.py
├── repositories/
│   ├── __init__.py
│   └── memo_repository.py
├── services/
│   ├── __init__.py
│   └── memo_service.py
├── routers/
│   ├── __init__.py
│   └── memo_router.py
└── templates/
    ├── base.html
    ├── home.html
    ├── list.html
    ├── detail.html
    ├── form.html
    └── not_found.html
```

## 모듈 구조와 각 모듈의 책임

### `memo_app.main`
- FastAPI 앱 생성
- 홈 화면 라우트(`GET /`) 제공
- 메모 라우터 등록
- 앱 시작 시 `init_db()` 호출로 DB 테이블 생성

### `memo_app.database`
- SQLite 엔진 생성
- SQLAlchemy 세션 팩토리(`SessionLocal`) 제공
- ORM Base 정의
- `init_db()`로 테이블 생성
- `get_db()`로 FastAPI `Depends`용 DB 세션 제공

### `memo_app.models.memo`
- `Memo` ORM 모델 정의
- 테이블명: `memos`
- 필드
  - `id`: 정수 PK, AUTOINCREMENT
  - `title`: 문자열
  - `content`: 문자열
  - `created_at`: 문자열

### `memo_app.schemas`
- 서비스 계층에서 사용하는 DTO 정의
- `MemoCreate`
- `MemoView`

### `memo_app.repositories.memo_repository`
- DB 접근 담당
- 메모 목록 조회
- 단건 조회
- 생성
- 수정
- 삭제
- 제목 기준 검색(`LIKE '%키워드%'`)

### `memo_app.services.memo_service`
- 비즈니스 로직 담당
- ORM 모델을 `MemoView`로 변환
- 등록/수정 시 입력값 검증
- `created_at` 생성
- 저장소 함수 호출 조합

### `memo_app.routers.memo_router`
- `/memos` 관련 요청/응답 처리
- 목록, 상세, 등록 폼, 수정 폼, 등록, 수정, 삭제 라우팅
- `TemplateResponse` 렌더링
- 등록/수정/삭제 후 `RedirectResponse(status_code=303)` 처리

### `memo_app.templates`
- 패키지 내부 `templates/` 디렉터리를 가리키는 `Jinja2Templates` 인스턴스 제공

### `memo_app/templates/*.html`
- `base.html`: 공통 레이아웃
- `home.html`: 홈 화면
- `list.html`: 메모 목록, 검색 폼
- `detail.html`: 메모 상세, 수정/삭제/목록 링크
- `form.html`: 등록/수정 공용 폼
- `not_found.html`: 없는 메모 안내 화면

## 설계 요약

- 도메인: 메모(Memo)
- DB 파일: 작업 폴더의 `database.db`
- DB URL: `sqlite:///database.db`
- 시드 데이터 없음
- `created_at`: `datetime.now().isoformat(timespec="seconds")`
- 존재하지 않는 메모 상세/수정 조회 시 `not_found.html`을 404로 렌더링
- 등록 성공 후 `/memos/{id}`로 303 리다이렉트
- 수정 성공 후 `/memos/{id}`로 303 리다이렉트
- 삭제 후 `/memos`로 303 리다이렉트
- 제목 또는 내용이 비어 있으면 400으로 폼 재렌더링
- 오류 메시지: `제목과 내용을 모두 입력하세요.`
- 검색: `GET /memos?q=키워드`

## 실행 방법

작업 폴더는 `memo_app` 패키지 바깥이어야 한다.

### 1. 가상환경 생성

```bash
python -m venv .venv
```

### 2. 가상환경 활성화

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. 패키지 설치

```bash
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart
```

### 4. 서버 실행

```bash
python -m uvicorn memo_app.main:app
```

기본 접속 주소:

```text
http://127.0.0.1:8000
```

## 주요 명령 예시와 실제 출력

### 문법 검사

실행 결과:

```text
[통과] py_compile
```

### 서버 기동

실행 결과:

```text
[통과] 서버 기동 http://127.0.0.1:49943
```

실행 명령:

```bash
python -m uvicorn memo_app.main:app
```

### 홈 화면 요청

요청:

```text
GET /
```

실제 결과:

```text
[통과] GET / -> 200
... 메모 앱 ... 메모 목록 보기 ... 새 메모 작성 ...
메모를 등록하고 목록, 상세, 수정, 삭제까지 할 수 있는 게시판형 웹 서비스입니다.
```

### 빈 입력 등록

요청:

```text
POST /memos
```

실제 결과:

```text
[통과] POST /memos -> 400
... 제목과 내용을 모두 입력하세요. ...
```

### 정상 등록

요청:

```text
POST /memos
```

실제 결과:

```text
[통과] POST /memos -> 303  Location: /memos/1
```

### 상세 조회

요청:

```text
GET /memos/1
```

실제 결과:

```text
[통과] GET /memos/1 -> 200
... 오늘 배운 것 정리 ...
... 내용: 라우터 서비스 저장소 분리 ...
```

### 검색

요청:

```text
GET /memos?q=할 일
```

실제 결과:

```text
[통과] GET /memos?q=할 일 -> 200
... 내일 할 일 ...
```

### 수정

요청:

```text
POST /memos/2/edit
```

실제 결과:

```text
[통과] POST /memos/2/edit -> 303  Location: /memos/2
```

수정 후 상세:

```text
[통과] GET /memos/2 -> 200
... 내일 할 일 수정됨 ...
... 내용: 실제로는 오늘 할 일 ...
```

### 삭제

요청:

```text
POST /memos/3/delete
```

실제 결과:

```text
[통과] POST /memos/3/delete -> 303  Location: /memos
```

### 없는 메모 조회

요청:

```text
GET /memos/999
```

실제 결과:

```text
[통과] GET /memos/999 -> 404
... 메모를 찾을 수 없습니다 ...
```

## 화면 흐름

### 홈
- `GET /`
- 앱 설명 문구 표시
- 링크
  - `/memos`
  - `/memos/new`

### 목록
- `GET /memos`
- 메모 목록 표시
- 검색 폼 제공
- 검색 시 `q` 쿼리 파라미터 사용

### 등록
- `GET /memos/new`
- 등록 폼 표시
- `POST /memos`
- 성공 시 `/memos/{id}`로 303 리다이렉트

### 상세
- `GET /memos/{memo_id}`
- 전체 필드 표시
  - ID
  - 제목
  - 작성일시
  - 내용
- 수정 링크, 삭제 버튼, 목록 링크 제공

### 수정
- `GET /memos/{memo_id}/edit`
- 수정 폼 표시
- `POST /memos/{memo_id}/edit`
- 성공 시 `/memos/{id}`로 303 리다이렉트

### 삭제
- `POST /memos/{memo_id}/delete`
- 성공 후 `/memos`로 303 리다이렉트

### 없는 데이터
- `GET /memos/{memo_id}`
- `GET /memos/{memo_id}/edit`
- 존재하지 않으면 `not_found.html`을 404로 렌더링

## 요구사항별 구현 위치

### 1. 서버 실행
- `memo_app.main`
- 실행 명령: `python -m uvicorn memo_app.main:app`

### 2. 프로젝트 구조 분리
- `routers/`: `memo_app/routers/memo_router.py`
- `services/`: `memo_app/services/memo_service.py`
- `repositories/`: `memo_app/repositories/memo_repository.py`
- `models/`: `memo_app/models/memo.py`
- 템플릿: `memo_app/templates/`

### 3. SSR 렌더링
- 홈: `memo_app.main`
- 메모 화면: `memo_app.routers.memo_router`
- 템플릿 파일:
  - `home.html`
  - `list.html`
  - `detail.html`
  - `form.html`
  - `not_found.html`

### 4. 홈 화면
- 라우트: `memo_app.main`
- 템플릿: `memo_app/templates/home.html`

### 5. 단일 모델 CRUD
- 모델: `memo_app/models/memo.py`
- 목록/상세/등록/수정/삭제 라우트: `memo_app/routers/memo_router.py`
- 저장소 CRUD: `memo_app/repositories/memo_repository.py`
- 비즈니스 처리: `memo_app/services/memo_service.py`

### 6. 폼 기반 입력/수정 처리
- 등록/수정 폼 템플릿: `memo_app/templates/form.html`
- `Form("")` 수신:
  - `memo_app/routers/memo_router.py`

### 7. Redirect 적용
- 등록 후 리다이렉트: `create_memo()`
- 수정 후 리다이렉트: `update_memo()`
- 삭제 후 리다이렉트: `delete_memo()`
- 위치: `memo_app/routers/memo_router.py`

### 8. 레이어 분리
- 라우터: `memo_app/routers/memo_router.py`
- 서비스: `memo_app/services/memo_service.py`
- 저장소: `memo_app/repositories/memo_repository.py`

### 9. SQLite + SQLAlchemy
- 엔진/세션/Base: `memo_app/database.py`
- ORM 모델: `memo_app/models/memo.py`
- 세션 주입: `get_db()` + `Depends`
- CRUD 쿼리: `memo_app/repositories/memo_repository.py`

## 라우트 목록

### 홈
- `GET /`

### 메모
- `GET /memos`
- `GET /memos/new`
- `POST /memos`
- `GET /memos/{memo_id}`
- `GET /memos/{memo_id}/edit`
- `POST /memos/{memo_id}/edit`
- `POST /memos/{memo_id}/delete`

## 데이터 모델

### Memo
- `id: int`
- `title: str`
- `content: str`
- `created_at: str`

## 검증과 예외 처리

- 등록/수정 시 `title.strip()` 또는 `content.strip()` 결과가 비어 있으면 실패
- 서비스 계층에서 `ValidationError` 발생
- 라우터에서 폼을 다시 렌더링하며 400 응답 반환
- 없는 메모는 404와 함께 `not_found.html` 렌더링

## DB 파일

앱 실행 후 작업 폴더에 다음 파일이 생성된다.

```text
database.db
```

이 파일에 메모 데이터가 저장된다.

## 구현 흐름

요청은 다음 순서로 처리된다.

1. 브라우저가 라우터에 요청
2. 라우터가 서비스 호출
3. 서비스가 검증 후 저장소 호출
4. 저장소가 SQLAlchemy 세션으로 SQLite 접근
5. 결과를 서비스가 `MemoView`로 변환
6. 라우터가 템플릿 렌더링 또는 리다이렉트 응답 반환

## 참고 사항

- 패키지 내부 import는 모두 상대 import를 사용한다.
- `TemplateResponse`는 `TemplateResponse(request, "이름.html", context)` 형식으로 호출한다.
- `Form("")` 기본값을 사용해 빈 입력을 422가 아니라 화면 검증 흐름으로 처리한다.
