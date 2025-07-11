from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerOut(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryOut(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderBase(BaseModel):
    customer_id: int
    status: str
    items: List[OrderItemBase]

class OrderOut(BaseModel):
    id: int
    order_date: datetime
    status: str
    customer: CustomerOut
    class Config:
        orm_mode = True