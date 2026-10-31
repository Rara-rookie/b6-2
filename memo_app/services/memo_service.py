from datetime import datetime

from sqlalchemy.orm import Session

from ..models.memo import Memo
from ..repositories import memo_repository
from ..schemas import MemoView


class ValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message: str = message


def to_view(memo: Memo) -> MemoView:
    return MemoView(
        id=memo.id,
        title=memo.title,
        content=memo.content,
        created_at=memo.created_at,
    )


def list_memos(db: Session, q: str | None = None) -> list[MemoView]:
    memos = memo_repository.list_memos(db, q)
    return [to_view(memo) for memo in memos]


def get_memo(db: Session, memo_id: int) -> MemoView | None:
    memo = memo_repository.get_memo(db, memo_id)
    if memo is None:
        return None
    return to_view(memo)


def create_memo(db: Session, title: str, content: str) -> MemoView:
    if not title.strip() or not content.strip():
        raise ValidationError("제목과 내용을 모두 입력하세요.")
    memo = memo_repository.create_memo(
        db,
        title=title,
        content=content,
        created_at=datetime.now().isoformat(timespec="seconds"),
    )
    return to_view(memo)


def update_memo(db: Session, memo_id: int, title: str, content: str) -> MemoView | None:
    if not title.strip() or not content.strip():
        raise ValidationError("제목과 내용을 모두 입력하세요.")
    memo = memo_repository.update_memo(db, memo_id, title, content)
    if memo is None:
        return None
    return to_view(memo)


def delete_memo(db: Session, memo_id: int) -> bool:
    return memo_repository.delete_memo(db, memo_id)
