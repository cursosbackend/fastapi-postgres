from fastapi import FastAPI, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from . import models, schemas



Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")


# ----------------- CLIENTES -----------------

@app.get("/customers")
def list_customers(request: Request, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.post("/customers")
def create_customer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    address: str = Form(""),
    db: Session = Depends(get_db)
):
    new_customer = models.Customer(name=name, email=email, phone=phone, address=address)
    db.add(new_customer)
    db.commit()
    return {"message": "Customer created"}

# ----------------- PRODUCTOS -----------------

@app.get("/products")
def list_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/products")
def create_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
    stock: int = Form(...),
    db: Session = Depends(get_db)
):
    product = models.Product(name=name, description=description, price=price, stock=stock)
    db.add(product)
    db.commit()
    return {"message": "Product created"}

# ----------------- ÓRDENES -----------------

@app.get("/orders")
def list_orders(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@app.post("/orders")
def create_order(
    customer_id: int = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    order = models.Order(customer_id=customer_id, status=status)
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"message": "Order created", "order_id": order.id}

@app.post("/orders/{order_id}/items")
def add_item_to_order(
    order_id: int,
    product_id: int = Form(...),
    quantity: int = Form(...),
    price: float = Form(...),
    db: Session = Depends(get_db)
):
    item = models.OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, price=price)
    db.add(item)
    db.commit()
    return {"message": "Item added"}

# ----------------- CATEGORÍAS -----------------

@app.get("/categories")
def list_categories(request: Request, db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories})

@app.post("/categories")
def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    return {"message": "Category created"}

@app.post("/products/{product_id}/add_category")
def assign_category_to_product(
    product_id: int,
    category_id: int = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).get(product_id)
    category = db.query(models.Category).get(category_id)
    if product and category:
        product.categories.append(category)
        db.commit()
        return {"message": "Category assigned"}
    return {"error": "Invalid IDs"}


