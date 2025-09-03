from fastapi import APIRouter, Request, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from database import Order, SessionLocal, Product
import shutil
import cloudinary.uploader
import io
import os
from PIL import Image

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

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

    # Open image with Pillow
    img = Image.open(file.file)

    # Resize if bigger than 1920px (example)
    img.thumbnail((1920, 1080))

    # Save to memory buffer as JPEG
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    # Upload smaller file to Cloudinary
    upload_result = cloudinary.uploader.upload(buffer)

    image_url = upload_result["secure_url"]



    # save product in DB with image URL
    new_product = Product(name=name, price=price, image=file.filename)
    db.add(new_product)
    db.commit()
    return RedirectResponse("/admin", status_code=302)