from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from database import Order, SessionLocal, Product


templates = Jinja2Templates(directory="templates")



router = APIRouter(
    prefix='/products',
    tags=['products']
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{product_id}/edit", response_class=HTMLResponse)
def edit_product(request: Request, product_id: int,  db: Session = Depends(get_db)):
    product = product = db.query(Product).filter(Product.id == product_id).first() # fetch product by ID
    return templates.TemplateResponse(
        "edit_product.html",
        {"request": request, "product": product}
    )
