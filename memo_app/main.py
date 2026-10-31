from fastapi import FastAPI, Request

from .database import init_db
from .routers.memo_router import router as memo_router
from .templates import templates

init_db()

app = FastAPI()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "request": request,
        },
    )


app.include_router(memo_router)
