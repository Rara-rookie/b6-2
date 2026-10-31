# memo_app 문서

## 개요

`memo_app`은 FastAPI, SQLAlchemy, Jinja2로 만든 서버 사이드 렌더링 기반 메모 게시판 웹 서비스다. 사용자는 홈 화면에서 메모 목록과 작성 화면으로 이동할 수 있고, 메모의 등록·목록 조회·상세 조회·수정·삭제를 브라우저 폼으로 수행할 수 있다.

- 패키지: `memo_app`
- 진입점: `memo_app.main`
- 실행 명령: `python -m uvicorn memo_app.main:app`
- 작업 폴더: 패키지 바깥
- DB 파일: 작업 폴더의 `database.db`
- 외부 패키지: `fastapi`, `uvicorn`, `sqlalchemy`, `jinja2`, `python-multipart`

패키지 내부 import는 모두 상대 import를 사용한다.

## 요구사항 분해

### 서버 실행
- FastAPI 앱이 `http://localhost:8000` 계열 주소에서 실행된다.
- 진입점 모듈은 `memo_app.main:app`이다.
- 앱 시작 시 `init_db()`를 호출해 테이블을 생성한다.

### 프로젝트 구조
다음 역할로 모듈이 분리되어 있다.

- `routers/`: HTTP 요청 처리, 화면 전환, PRG 적용
- `services/`: 검증과 비즈니스 로직
- `repositories/`: SQLAlchemy 세션 기반 DB 접근
- `models/`: ORM 모델
- `templates/`: Jinja2 템플릿
- `database.py`: 엔진, 세션 팩토리, DB 의존성
- `templates.py`: 템플릿 로더
- `schemas.py`: 화면 전달용 DTO

### 화면 렌더링
주요 화면은 모두 `Jinja2Templates.TemplateResponse`로 렌더링된다.

- 홈: `templates/home.html`
- 목록: `templates/list.html`
- 상세: `templates/detail.html`
- 등록/수정 폼: `templates/form.html`
- 없음 안내: `templates/not_found.html`

### 도메인
단일 도메인은 `Memo`다.

필드:
- `id: int`
- `title: str`
- `content: str`
- `created_at: str`

설계:
- `id`는 SQLite AUTOINCREMENT 정수 PK
- `created_at`은 `datetime.now().isoformat(timespec="seconds")` 문자열로 저장
- 시드 데이터는 없다

### CRUD 흐름
- 목록 조회: `GET /memos`
- 검색: `GET /memos?q=키워드`
- 상세 조회: `GET /memos/{memo_id}`
- 등록 폼: `GET /memos/new`
- 등록 처리: `POST /memos`
- 수정 폼: `GET /memos/{memo_id}/edit`
- 수정 처리: `POST /memos/{memo_id}/edit`
- 삭제 처리: `POST /memos/{memo_id}/delete`

### PRG 적용
등록·수정·삭제 성공 후 즉시 템플릿을 렌더링하지 않고 303 리다이렉트를 사용한다.

- 등록 성공 후: `GET /memos/{id}`
- 수정 성공 후: `GET /memos/{id}`
- 삭제 성공 후: `GET /memos`

### 검증과 오류 처리
- 등록/수정 시 `title` 또는 `content`가 비어 있으면 폼을 `400`으로 다시 렌더링한다.
- 오류 메시지: `제목과 내용을 모두 입력하세요.`
- 존재하지 않는 메모의 상세/수정 조회는 `templates/not_found.html`을 `404`로 렌더링한다.
- 수정 처리에서 대상이 없으면 `404`를 렌더링한다.
- 삭제 처리에서는 존재 여부와 무관하게 목록으로 `303` 리다이렉트한다.

## 모듈 계약과 설계 결정

## 설계 결정

### 기술 선택
- 웹 프레임워크: FastAPI
- 템플릿: Jinja2
- DB: SQLite
- ORM: SQLAlchemy Session

### 템플릿 호출 방식
`starlette` 환경에서는 `TemplateResponse(request, "이름.html", context)` 순서만 사용한다. 이 앱도 그 형식으로 통일되어 있다.

### Form 처리 방식
`fastapi`의 `Form(...)` 필수값 방식은 빈 입력 시 핸들러 전에 422 JSON이 반환될 수 있으므로, 이 앱은 `Form("")`를 사용해 라우터까지 요청을 받는다. 이후 서비스에서 직접 검증하고 폼 화면에 오류 메시지를 표시한다.

### 검색 방식
목록 검색은 제목 기준 부분 일치다.

- 쿼리 파라미터: `q`
- 저장소 쿼리: `Memo.title.like(f"%{q}%")`

### 데이터 정렬
목록은 `id` 내림차순으로 보여 준다.

## 모듈 계약

### `__init__.py`
패키지 마커.

### `database.py`
SQLAlchemy 엔진, 세션 팩토리, Base, DB 초기화와 의존성 제공.

구성:
- `engine`
- `SessionLocal`
- `Base`
- `init_db() -> None`
- `get_db() -> Iterator[Session]`

특징:
- 연결 문자열: `sqlite:///database.db`
- `check_same_thread=False`

### `models/memo.py`
`Memo` ORM 모델 정의.

- 테이블명: `memos`
- `sqlite_autoincrement=True`

컬럼:
- `id`
- `title`
- `content`
- `created_at`

### `schemas.py`
화면 전달용 DTO.

- `MemoCreate(title, content)`
- `MemoView(id, title, content, created_at)`

실제 서비스 로직에서는 `MemoView`를 사용해 ORM 객체를 화면용 객체로 변환한다.

### `repositories/memo_repository.py`
DB 접근 전담.

함수:
- `list_memos(db, q=None) -> list[Memo]`
- `get_memo(db, memo_id) -> Memo | None`
- `create_memo(db, title, content, created_at) -> Memo`
- `update_memo(db, memo_id, title, content) -> Memo | None`
- `delete_memo(db, memo_id) -> bool`

책임:
- 쿼리 작성
- `commit`, `refresh`, `delete`
- 존재 여부 판단

### `services/memo_service.py`
비즈니스 로직과 검증 전담.

구성:
- `ValidationError`
- `to_view(memo) -> MemoView`
- `list_memos(db, q=None) -> list[MemoView]`
- `get_memo(db, memo_id) -> MemoView | None`
- `create_memo(db, title, content) -> MemoView`
- `update_memo(db, memo_id, title, content) -> MemoView | None`
- `delete_memo(db, memo_id) -> bool`

책임:
- 제목/내용 공백 검증
- `created_at` 생성
- ORM 모델을 `MemoView`로 변환

### `routers/memo_router.py`
메모 관련 화면 라우팅과 PRG 처리.

라우트:
- `GET /memos`
- `GET /memos/new`
- `POST /memos`
- `GET /memos/{memo_id}`
- `GET /memos/{memo_id}/edit`
- `POST /memos/{memo_id}/edit`
- `POST /memos/{memo_id}/delete`

책임:
- `Request`, `Form`, `Depends(get_db)` 처리
- 서비스 호출
- `TemplateResponse`와 `RedirectResponse(status_code=303)` 반환
- `400`, `404` 상태 코드 지정

### `templates.py`
`__file__` 기준 `templates/` 경로를 계산해 `Jinja2Templates` 인스턴스를 제공한다.

### `main.py`
앱 조립 루트.

역할:
- `init_db()` 호출
- `FastAPI()` 생성
- 홈 라우트 `GET /`
- 메모 라우터 등록

## 요청 처리 흐름

### 홈 화면
1. 브라우저가 `GET /` 요청
2. `main.py`의 `home()` 실행
3. `home.html` 렌더링
4. 메모 목록 보기, 새 메모 작성 링크 제공

### 목록 조회
1. 브라우저가 `GET /memos` 또는 `GET /memos?q=...` 요청
2. 라우터가 `q`와 DB 세션을 받음
3. 서비스가 저장소 호출
4. 저장소가 SQLAlchemy로 메모 목록 조회
5. 서비스가 `MemoView` 목록으로 변환
6. `list.html` 렌더링

### 등록
1. 브라우저가 `GET /memos/new` 요청
2. `form.html`을 생성 모드로 렌더링
3. 사용자가 폼 제출
4. `POST /memos`
5. 서비스가 공백 검증
6. 성공 시 저장소가 DB 저장
7. 라우터가 `303`으로 `/memos/{id}` 리다이렉트
8. 브라우저가 상세 페이지 `GET` 요청

### 수정
1. 브라우저가 `GET /memos/{id}/edit` 요청
2. 존재하면 수정 폼 렌더링, 없으면 `404`
3. 사용자가 폼 제출
4. `POST /memos/{id}/edit`
5. 서비스가 공백 검증
6. 저장소가 업데이트
7. 성공 시 `303`으로 상세 페이지 리다이렉트

### 삭제
1. 상세 화면의 삭제 폼 제출
2. `POST /memos/{id}/delete`
3. 서비스와 저장소가 삭제 시도
4. 라우터가 `303`으로 `/memos` 리다이렉트

## 디렉터리 구조

- `memo_app/__init__.py`
- `memo_app/database.py`
- `memo_app/main.py`
- `memo_app/templates.py`
- `memo_app/schemas.py`
- `memo_app/models/__init__.py`
- `memo_app/models/memo.py`
- `memo_app/repositories/__init__.py`
- `memo_app/repositories/memo_repository.py`
- `memo_app/services/__init__.py`
- `memo_app/services/memo_service.py`
- `memo_app/routers/__init__.py`
- `memo_app/routers/memo_router.py`
- `memo_app/templates/base.html`
- `memo_app/templates/home.html`
- `memo_app/templates/list.html`
- `memo_app/templates/detail.html`
- `memo_app/templates/form.html`
- `memo_app/templates/not_found.html`

## 실행 방법

### 1. 가상환경 생성 및 활성화
환경에 맞는 방식으로 Python 가상환경을 만든다.

### 2. 패키지 설치
필수 패키지:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `jinja2`
- `python-multipart`

### 3. 서버 실행
패키지 바깥 작업 폴더에서 실행:

`python -m uvicorn memo_app.main:app`

### 4. 접속
- 홈: `http://localhost:8000/`
- 목록: `http://localhost:8000/memos`

앱 실행 시 작업 폴더에 `database.db` 파일이 생성된다.

## 단계별 실행 계획

### 1단계: 기반 구성
- `memo_app` 패키지 생성
- 상대 import 규칙 적용
- `database.py`에서 엔진, 세션, Base, `init_db()`, `get_db()` 구성
- `templates.py`에서 템플릿 로더 구성

### 2단계: 도메인 모델 정의
- `models/memo.py`에 `Memo` ORM 모델 정의
- `id`, `title`, `content`, `created_at` 컬럼 구성
- AUTOINCREMENT 적용

### 3단계: 저장소 구현
- 메모 목록 조회
- 단건 조회
- 생성
- 수정
- 삭제
- 제목 LIKE 검색 추가

### 4단계: 서비스 구현
- `MemoView` 변환 함수 작성
- 등록/수정 공백 검증 추가
- `created_at` 생성 규칙 반영

### 5단계: 라우터 구현
- 홈 외 메모 CRUD 라우트 작성
- `Depends(get_db)`로 세션 주입
- `Form("")`로 폼 입력 수신
- 성공 시 303 리다이렉트
- 실패 시 400/404 템플릿 렌더링

### 6단계: 템플릿 구현
- 공통 레이아웃 작성
- 홈 화면 작성
- 목록 및 검색 폼 작성
- 상세 화면의 수정/삭제/목록 링크 작성
- 등록/수정 공용 폼 작성
- 없음 안내 화면 작성

### 7단계: 앱 조립
- `main.py`에서 `init_db()` 호출
- `FastAPI` 앱 생성
- 홈 라우트 추가
- 메모 라우터 등록

### 8단계: 검증 및 수동 시험
- 컴파일 확인
- 서버 기동 확인
- 홈/목록/등록/수정/삭제/검색/404 흐름 확인

## 인수 시험 목록과 각 시험이 확인하는 것

### 1. `GET /` → `200`
확인:
- 홈 화면이 정상 렌더링되는가
- `새 메모 작성` 링크가 있는가
- 앱 목적 설명이 보이는가

### 2. `GET /memos` → `200`
확인:
- 목록 화면이 정상 렌더링되는가
- 빈 테이블 시작 상태에서 `메모가 없습니다.`가 보이는가

### 3. `POST /memos` → `400`
확인:
- 제목 또는 내용이 비어 있을 때 422가 아니라 폼 화면으로 돌아오는가
- 오류 메시지 `제목과 내용을 모두 입력하세요.`가 표시되는가

### 4. `POST /memos` → `400`
확인:
- 다른 빈 입력 케이스도 동일하게 서버 검증으로 처리되는가
- 입력값이 폼에 다시 채워져 렌더링되는가

### 5. `POST /memos` → `303` / `Location: /memos/1`
확인:
- 첫 메모가 생성되는가
- PRG 패턴이 적용되는가
- ID가 1부터 증가하는가

### 6. `GET /memos/1` → `200`
확인:
- 상세 화면이 정상 렌더링되는가
- 전체 필드 `id`, `title`, `created_at`, `content`가 보이는가
- 저장된 내용 `라우터 서비스 저장소 분리`가 반영되는가

### 7. `POST /memos` → `303` / `Location: /memos/2`
확인:
- 두 번째 메모 생성과 ID 증가가 동작하는가

### 8. `POST /memos` → `303` / `Location: /memos/3`
확인:
- 세 번째 메모 생성과 누적 저장이 동작하는가

### 9. `GET /memos` → `200`
확인:
- 목록에 여러 메모가 표시되는가
- 최신 메모가 먼저 보이는가
- `장보기 목록`이 목록에 포함되는가

### 10. `GET /memos?q=할 일` → `200`
확인:
- 제목 검색이 동작하는가
- `내일 할 일`이 필터링되어 보이는가
- 검색 상태에서 `전체 보기` 링크가 보이는가

### 11. `POST /memos/2/edit` → `303` / `Location: /memos/2`
확인:
- 수정 성공 시 상세 페이지로 리다이렉트되는가
- PRG가 수정에도 적용되는가

### 12. `GET /memos/2` → `200`
확인:
- 수정 결과가 DB에 반영되었는가
- 내용이 `실제로는 오늘 할 일`로 바뀌었는가

### 13. `POST /memos/2/edit` → `400`
확인:
- 수정 시에도 공백 검증이 같은 규칙으로 동작하는가
- 오류 메시지와 기존 입력값 재표시가 되는가

### 14. `POST /memos/3/delete` → `303` / `Location: /memos`
확인:
- 삭제 성공 후 목록으로 리다이렉트되는가
- 삭제에도 PRG가 적용되는가

### 15. `GET /memos/3` → `404`
확인:
- 삭제된 메모 접근 시 없음 안내 화면이 렌더링되는가
- 상태 코드가 404인가

### 16. `GET /memos/999` → `404`
확인:
- 존재하지 않는 임의 ID도 동일하게 처리되는가
- `찾을 수 없습니다` 안내가 보이는가

### 보조 확인
- `py_compile` 통과
- 서버 기동 성공

## 위험 요소와 대응

### 1. Form 필수 처리로 인한 422 JSON 응답
위험:
- `Form(...)`를 쓰면 빈 값이 라우터에 도달하기 전에 422로 처리될 수 있다.

대응:
- `title`, `content`를 `Form("")`로 받고 서비스에서 `strip()` 검증을 수행한다.
- 실패 시 `400` 폼 재렌더링과 오류 메시지를 제공한다.

### 2. TemplateResponse 호출 형식 오류
위험:
- 옛 형식으로 호출하면 런타임 500이 발생할 수 있다.

대응:
- 모든 템플릿 렌더링을 `TemplateResponse(request, "파일명.html", context)` 형식으로 통일한다.

### 3. 라우터에 비즈니스 로직이 섞이는 문제
위험:
- 검증, 시간 생성, 변
