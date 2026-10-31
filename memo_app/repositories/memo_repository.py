from sqlalchemy.orm import Session

from ..models.memo import Memo


def list_memos(db: Session, q: str | None = None) -> list[Memo]:
    query = db.query(Memo)
    if q:
        query = query.filter(Memo.title.like(f"%{q}%"))
    return query.order_by(Memo.id.desc()).all()


def get_memo(db: Session, memo_id: int) -> Memo | None:
    return db.query(Memo).filter(Memo.id == memo_id).first()


def create_memo(db: Session, title: str, content: str, created_at: str) -> Memo:
    memo = Memo(title=title, content=content, created_at=created_at)
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def update_memo(db: Session, memo_id: int, title: str, content: str) -> Memo | None:
    memo = get_memo(db, memo_id)
    if memo is None:
        return None
    memo.title = title
    memo.content = content
    db.commit()
    db.refresh(memo)
    return memo


def delete_memo(db: Session, memo_id: int) -> bool:
    memo = get_memo(db, memo_id)
    if memo is None:
        return False
    db.delete(memo)
    db.commit()
    return True
