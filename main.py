import shutil
import json
import redis.asyncio as redis
from fastapi import FastAPI, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, Product, Order, User
from routers import cart, order, auth, admin, product
from middleware import AuthMiddleware, get_current_user_from_cookie
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add authentication middleware
app.add_middleware(AuthMiddleware, protected_paths=["/admin"])

templates = Jinja2Templates(directory="templates")
USE_DOCKER = os.getenv("USE_DOCKER", "False") == "True"

# connect to Redis (default port is 6379)
REDIS_URL = os.getenv("REDIS_URL_DOCKER") if USE_DOCKER else os.getenv("REDIS_URL_LOCAL")
print("REDIS_URL = ", REDIS_URL)
redis_client = redis.Redis.from_url(REDIS_URL)
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
    
    # Get current user if authenticated
    current_user = None
    try:
        current_user = get_current_user_from_cookie(request)
    except:
        pass  # User not authenticated
    
    return templates.TemplateResponse("index.html", {"request": request, "products": products, "current_user": current_user})


app.include_router(cart.router)
app.include_router(order.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(product.router)