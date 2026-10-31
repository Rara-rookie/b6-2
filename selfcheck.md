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
