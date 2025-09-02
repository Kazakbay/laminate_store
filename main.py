import shutil
import json
import redis.asyncio as redis
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, Product, Order
from routers import cart, order, auth, admin


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

# connect to Redis (default port is 6379)
redis_client = redis.Redis(host="redis", port=6379, db=0)
# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # check cache
    cached_products = await redis_client.get("products")
    if cached_products:
        products = json.loads(cached_products)
    else:
        # query DB if not in cache
        db_products = db.query(Product).all()
        products = [{"id": p.id, "name": p.name, "price": p.price, "image":p.image} for p in db_products]
        # save to cache for 60 sec
        await redis_client.set("products", json.dumps(products), ex=60)
    return templates.TemplateResponse("index.html", {"request": request, "products": products})


app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(auth.router)