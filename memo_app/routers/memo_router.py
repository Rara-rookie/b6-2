from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import memo_service
from ..templates import templates

router = APIRouter(prefix="/memos", tags=["memos"])


@router.get("")
def list_memos(request: Request, q: str | None = None, db: Session = Depends(get_db)):
    memos = memo_service.list_memos(db, q)
    return templates.TemplateResponse(
        request,
        "list.html",
        {
            "memos": memos,
            "q": q or "",
        },
    )


@router.get("/new")
def new_memo_form(request: Request):
    return templates.TemplateResponse(
        request,
        "form.html",
        {
            "mode": "create",
            "memo": None,
            "error": None,
            "action": "/memos",
        },
    )


@router.post("")
def create_memo(
    request: Request,
    title: str = Form(""),
    content: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        memo = memo_service.create_memo(db, title, content)
    except memo_service.ValidationError as exc:
        return templates.TemplateResponse(
            request,
            "form.html",
            {
                "mode": "create",
                "memo": {"title": title, "content": content},
                "error": exc.message,
                "action": "/memos",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return RedirectResponse(
        url=f"/memos/{memo.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/{memo_id}")
def get_memo_detail(request: Request, memo_id: int, db: Session = Depends(get_db)):
    memo = memo_service.get_memo(db, memo_id)
    if memo is None:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return templates.TemplateResponse(
        request,
        "detail.html",
        {
            "memo": memo,
        },
    )


@router.get("/{memo_id}/edit")
def edit_memo_form(request: Request, memo_id: int, db: Session = Depends(get_db)):
    memo = memo_service.get_memo(db, memo_id)
    if memo is None:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return templates.TemplateResponse(
        request,
        "form.html",
        {
            "mode": "edit",
            "memo": memo,
            "error": None,
            "action": f"/memos/{memo_id}/edit",
        },
    )


@router.post("/{memo_id}/edit")
def update_memo(
    request: Request,
    memo_id: int,
    title: str = Form(""),
    content: str = Form(""),
    db: Session = Depends(get_db),
):
    try:
        memo = memo_service.update_memo(db, memo_id, title, content)
    except memo_service.ValidationError as exc:
        return templates.TemplateResponse(
            request,
            "form.html",
            {
                "mode": "edit",
                "memo": {"id": memo_id, "title": title, "content": content},
                "error": exc.message,
                "action": f"/memos/{memo_id}/edit",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if memo is None:
        return templates.TemplateResponse(
            request,
            "not_found.html",
            {},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return RedirectResponse(
        url=f"/memos/{memo.id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/{memo_id}/delete")
def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    memo_service.delete_memo(db, memo_id)
    return RedirectResponse(
        url="/memos",
        status_code=status.HTTP_303_SEE_OTHER,
    )
