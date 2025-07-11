from sqlalchemy import Column, Integer, Table ,BigInteger,ForeignKey,Text, DateTime, Numeric
from sqlalchemy.orm import  relationship 
from .database import Base
from datetime import datetime





product_categories = Table(
    'product_categories', Base.metadata,
    Column('product_id', BigInteger, ForeignKey('products.id'), primary_key=True),
    Column('category_id', BigInteger, ForeignKey('categories.id'), primary_key=True)
)



class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    phone = Column(Text)
    address = Column(Text)
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = 'products'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    categories = relationship("Category", secondary=product_categories, back_populates="products")

class Category(Base):
    __tablename__ = 'categories'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, nullable=False)
    products = relationship("Product", secondary=product_categories, back_populates="categories")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True)
    customer_id = Column(BigInteger, ForeignKey("customers.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Text, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, ForeignKey("orders.id"))
    product_id = Column(BigInteger, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")