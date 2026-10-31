from sqlalchemy import Column, Integer, String

from ..database import Base


class Memo(Base):
    __tablename__ = "memos"
    __table_args__ = {"sqlite_autoincrement": True}

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    created_at: str = Column(String, nullable=False)
