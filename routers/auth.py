from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.get("/login", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

