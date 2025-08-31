from fastapi import APIRouter, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from database import Order, SessionLocal

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/order',
    tags=['order']
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def order_form(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})

@router.post("/")
async def place_order(
    name: str = Form(...), phone: str = Form(...), address: str = Form(...),
    db: Session = Depends(get_db)
):
    new_order = Order(customer_name=name, phone=phone, address=address)
    db.add(new_order)
    db.commit()
    return RedirectResponse("/", status_code=302)