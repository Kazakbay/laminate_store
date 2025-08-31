from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database import Order, SessionLocal, Product
import shutil

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Admin Panel ----------
@router.get("/", response_class=HTMLResponse)
async def admin(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    orders = db.query(Order).all()
    return templates.TemplateResponse("admin.html", {"request": request, "products": products, "orders": orders})

@router.get("/add", response_class=HTMLResponse)
async def add_product_form(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@router.post("/add")
async def add_product(
    name: str = Form(...), price: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    # save the image to the uploads folder
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_product = Product(name=name, price=price, image=file.filename)
    db.add(new_product)
    db.commit()
    return RedirectResponse("/admin", status_code=302)