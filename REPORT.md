# 판정 보고서

| 항목 | 결과 |
|---|---|
| 인수 시험 | 전부 통과 |
| 자기 점검 미흡 | 1건 |
| 사람 확인 필요 | 0건 |
| 모듈 / 줄 수 | 19개 / 510줄 |
| 요구사항 커버리지 | 9개 중 7개 시험됨 |
| 이번 실행 차감 | 49,107 |

## 어느 시험도 건드리지 않은 요구사항

- 2
- 8

## 설계 결정

- 도메인은 메모(Memo). 필드: id(int PK, 1부터 증가), title(str), content(str), created_at(str ISO)
- created_at 은 datetime.now().isoformat(timespec='seconds') 로 저장
- DB 파일은 작업 폴더의 database.db (sqlite:///database.db)
- 시드 데이터 없음. 앱 시작 시 빈 테이블로 시작한다
- id 는 SQLite AUTOINCREMENT 로 1부터 증가하는 정수
- 존재하지 않는 메모 상세/수정 조회 시 templates/not_found.html 을 status_code=404 로 렌더한다
- 등록 성공 후 GET /memos/{id} 로 303 리다이렉트, 수정 성공 후 GET /memos/{id} 로 303, 삭제 성공 후 GET /memos 로 303
- 빈 title 또는 빈 content 로 등록/수정 시 폼을 status_code=400 으로 다시 렌더하며 error 메시지 '제목과 내용을 모두 입력하세요.' 를 표시(리다이렉트 안 함)
- 목록 검색은 GET /memos?q=키워드 로 title LIKE '%키워드%' 필터. q 없으면 전체
- 홈 GET / 은 templates/home.html 렌더, '메모 목록 보기'(/memos)와 '새 메모 작성'(/memos/new) 링크 포함

## 인수 시험 결과

```
[통과] py_compile


[통과] 서버 기동 http://127.0.0.1:49943

[통과] GET / -> 200
홈 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 앱 메모를 등록하고 목록, 상세, 수정, 삭제까지 할 수 있는 게시판형 웹 서비스입니다. 브라우저에서 메모를 작성하고 관리해 보세요. 메모 목록 보기 새 메모 작성 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] GET /memos -> 200
메모 목록 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 목록 검색 메모가 없습니다. 새 메모 작성 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos -> 400
새 메모 작성 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 새 메모 작성 제목과 내용을 모두 입력하세요. 제목 내용 내용만 있음 저장 취소 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos -> 400
새 메모 작성 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 새 메모 작성 제목과 내용을 모두 입력하세요. 제목 내용 저장 취소 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos -> 303  Location: /memos/1


[통과] GET /memos/1 -> 200
메모 상세 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 상세 오늘 배운 것 정리 ID: 1 작성일시: 2026-09-15T12:33:48 내용: 라우터 서비스 저장소 분리 수정 삭제 목록으로 돌아가기 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos -> 303  Location: /memos/2


[통과] POST /memos -> 303  Location: /memos/3


[통과] GET /memos -> 200
메모 목록 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 목록 검색 장보기 목록 상세보기 내일 할 일 상세보기 오늘 배운 것 정리 상세보기 새 메모 작성 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] GET /memos?q=할 일 -> 200
메모 목록 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 목록 검색 전체 보기 내일 할 일 상세보기 새 메모 작성 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos/2/edit -> 303  Location: /memos/2


[통과] GET /memos/2 -> 200
메모 상세 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 상세 내일 할 일 수정됨 ID: 2 작성일시: 2026-09-15T12:33:48 내용: 실제로는 오늘 할 일 수정 삭제 목록으로 돌아가기 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos/2/edit -> 400
메모 수정 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모 수정 제목과 내용을 모두 입력하세요. 제목 내용 빈 제목 수정 저장 취소 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] POST /memos/3/delete -> 303  Location: /memos


[통과] GET /memos/3 -> 404
메모를 찾을 수 없습니다 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모를 찾을 수 없습니다 요청하신 메모가 존재하지 않거나 이미 삭제되었습니다. 메모 목록으로 돌아가기 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스

[통과] GET /memos/999 -> 404
메모를 찾을 수 없습니다 body { font-family: sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; line-height: 1.6; color: #222; } header, footer { margin-bottom: 24px; } nav a { margin-right: 12px; } .error { color: #b00020; font-weight: bold; } form { margin: 16px 0; } input[type="text"], textarea { width: 100%; max-width: 100%; box-sizing: border-box; padding: 8px; } textarea { min-height: 180px; } .actions { margin-top: 16px; } .actions a, .actions button { margin-right: 8px; } 메모 앱 메모 목록 보기 새 메모 작성 메모를 찾을 수 없습니다 요청하신 메모가 존재하지 않거나 이미 삭제되었습니다. 메모 목록으로 돌아가기 FastAPI와 SQLAlchemy로 만든 게시판형 메모 서비스
```

## 자기 점검

| 요구사항 | 상태 | 근거 |
|---|---|---|
| GET / 홈 화면 렌더링 + 앱 설명 + 링크 2개 이상 | 충족 | `GET / -> 200`, home.html에 `메모를 등록하고 목록, 상세, 수정, 삭제까지 할 수 있는 게시판형 웹 서비스입니다.` 문구와 `/memos`, `/memos/new` 링크 2개 존재 |
| 단일 도메인 CRUD 화면 흐름(등록/목록/상세/수정/삭제) SSR | 충족 | `memo_router.py`에 list/new/create/detail/edit/update/delete 라우트, 각 TemplateResponse 렌더링, 실행 결과 `GET /memos`, `GET /memos/1`, 수정/삭제 모두 통과 |
| POST → Redirect → GET(303) 적용 | 충족 | `POST /memos -> 303 Location:/memos/1`, `POST /memos/2/edit -> 303`, `POST /memos/3/delete -> 303`, 모두 `status.HTTP_303_SEE_OTHER` |
| 레이어 분리(라우터/서비스/저장소) | 충족 | `routers/memo_router.py`가 서비스 호출, `services/memo_service.py`가 검증·변환, `repositories/memo_repository.py`가 DB 접근 담당 |
| models/ SQLAlchemy ORM 모델 클래스 분리 | 충족 | `models/memo.py`의 `class Memo(Base)` 컬럼 정의 |
| templates/ 디렉터리 존재 | 충족 | `templates/` 아래 base/home/list/detail/form/not_found.html 존재 |
| requirements.txt 또는 pyproject.toml 의존성 명시 | 미흡 | 구현 파일 목록에 `requirements.txt`/`pyproject.toml` 없음. 의존성은 README 본문에만 서술 |
| 모든 주요 화면 TemplateResponse로 렌더링 | 충족 | main.py 홈과 memo_router 전 화면이 `templates.TemplateResponse` 사용 |
| 상세 화면에 전체 필드 표시 | 충족 | detail.html에 `memo.id`, `memo.title`, `memo.created_at`, `memo.content` 표시, `GET /memos/1`에 ID/작성일시/내용 출력 |
| 상세에 수정/삭제/목록 링크 | 충족 | detail.html에 `/memos/{id}/edit`, delete form, `/memos` 링크 존재 |
| 존재하지 않는 데이터 조회 시 안내 화면 | 충족 | `GET /memos/999 -> 404` not_found.html `메모를 찾을 수 없습니다` 출력 |
| 폼 입력 필드+저장 버튼+취소 링크 | 충족 | form.html에 title input, content textarea, 저장 버튼, `/memos` 취소 링크 |
| 등록/수정 POST 방식 처리 | 충족 | `@router.post("")`, `@router.post("/{memo_id}/edit")` |
| 폼 데이터 Form()으로 수신 | 충족 | `title: str = Form("")`, `content: str = Form("")` |
| 새로고침 중복 방지(PRG) | 충족 | 등록/수정/삭제 모두 303 리다이렉트로 GET 화면 이동 |
| DB 접근이 Repository에 존재 | 충족 | `repositories/memo_repository.py`에서 `db.query`, `db.add`, `db.commit`, `db.delete` |
| SQLite + SQLAlchemy 저장, 메모리 저장 금지 | 충족 | `create_engine("sqlite:///database.db")`, 저장소 CRUD가 Session 기반 |
| SQLAlchemy Session 사용 | 충족 | `SessionLocal = sessionmaker(...)`, repository 함수가 Session 인자 사용 |
| DB 세션 Depends 의존성 주입 | 충족 | `get_db()` + 라우터 `db: Session = Depends(get_db)` |
| database.db 파일 생성 | 충족 | `init_db()` → `Base.metadata.create_all`, URL `sqlite:///database.db`, 서버 기동 통과 |
| README.md(가상환경/설치/실행 순서) | 충족 | README에 venv 생성·활성화·pip install·`python -m uvicorn memo_app.main:app` 순서 명시 |
| 보너스: 검색 기능(쿼리 파라미터+like) | 충족 | `GET /memos?q=할 일 -> 200`에 `내일 할 일` 필터링, repository `Memo.title.like(f"%{q}%")` |
| 보너스: 필수값 검증 | 충족 | `POST /memos -> 400` `제목과 내용을 모두 입력하세요.`, service `ValidationError` |
| 권장: ORM 모델 직접 반환 대신 DTO 분리 | 충족 | `schemas.py`의 MemoView, service `to_view()`로 변환 후 반환 |
