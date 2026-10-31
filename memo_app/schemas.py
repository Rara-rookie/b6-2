class MemoCreate:
    def __init__(self, title: str, content: str):
        self.title: str = title
        self.content: str = content


class MemoView:
    def __init__(self, id: int, title: str, content: str, created_at: str):
        self.id: int = id
        self.title: str = title
        self.content: str = content
        self.created_at: str = created_at
