from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, Product, Order

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/order", response_class=HTMLResponse)
async def order_form(request: Request):
    return templates.TemplateResponse("order.html", {"request": request})

@app.post("/order")
async def place_order(
    name: str = Form(...), phone: str = Form(...), address: str = Form(...),
    db: Session = Depends(get_db)
):
    new_order = Order(customer_name=name, phone=phone, address=address)
    db.add(new_order)
    db.commit()
    return RedirectResponse("/", status_code=302)

# ---------- Admin Panel ----------
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    orders = db.query(Order).all()
    return templates.TemplateResponse("admin.html", {"request": request, "products": products, "orders": orders})

@app.get("/admin/add", response_class=HTMLResponse)
async def add_product_form(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.post("/admin/add")
async def add_product(
    name: str = Form(...), price: int = Form(...), image: str = Form(...),
    db: Session = Depends(get_db)
):
    new_product = Product(name=name, price=price, image=image)
    db.add(new_product)
    db.commit()
    return RedirectResponse("/admin", status_code=302)
