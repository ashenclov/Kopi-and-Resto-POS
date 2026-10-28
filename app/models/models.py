from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String(50), unique=True, nullable=False)
    capacity = Column(Integer, default=4)
    status = Column(String(20), default="available")  # available, occupied, reserved

    orders = relationship("Order", back_populates="table")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    icon = Column(String(50), default="utensils")
    display_order = Column(Integer, default=0)

    menus = relationship("Menu", back_populates="category", cascade="all, delete-orphan")


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(255), default="")

    category = relationship("Category", back_populates="menus")
    order_items = relationship("OrderItem", back_populates="menu")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    order_type = Column(String(20), default="dine_in")  # dine_in, takeaway
    customer_name = Column(String(100), default="Pelanggan")
    status = Column(String(20), default="active")  # active, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float, default=0.0)

    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    notes = Column(String(255), default="")
    status = Column(String(20), default="pending")  # pending, cooking, served

    order = relationship("Order", back_populates="items")
    menu = relationship("Menu", back_populates="order_items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    payment_time = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(30), default="cash")  # cash, qris, transfer
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    final_amount = Column(Float, default=0.0)
    pay_amount = Column(Float, default=0.0)
    change_amount = Column(Float, default=0.0)
    cashier_name = Column(String(100), default="Kasir")

    order = relationship("Order", back_populates="payment")
