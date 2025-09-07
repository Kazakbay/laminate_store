from PIL import Image
from fastapi import FastAPI, Request, APIRouter, Depends, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import cloudinary.uploader
from starlette.responses import RedirectResponse

from database import Order, SessionLocal, Product
import io
import os
templates = Jinja2Templates(directory="templates")

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


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
    product = db.query(Product).filter(Product.id == product_id).first() # fetch product by ID
    return templates.TemplateResponse(
        "edit_product.html",
        {"request": request, "product": product}
    )

@router.post("/{product_id}/update", response_class=HTMLResponse)
def update_product(
    request: Request,                      # <-- add request
    product_id: int,
    name: str = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),         # <-- match HTML field
    db: Session = Depends(get_db)
):
    # Open and resize
    img = Image.open(image.file)
    img.thumbnail((1920, 1080))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    buffer.seek(0)

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(buffer)
    image_url = upload_result["secure_url"]


    # Update product
    product = db.query(Product).filter(Product.id == product_id).first()
    if product.image_public_id:
        cloudinary.uploader.destroy(product.image_public_id)

    product.name = name
    product.price = price
    product.image = image_url
    product.image_public_id = upload_result["public_id"]

    db.commit()

    return RedirectResponse("/admin", status_code=302)