from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path
from datetime import datetime, date

from app.database import get_db
from app.models.models import Table, Category, Menu, Order, OrderItem, Payment
from app.config import APP_NAME, TAX_RATE

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["Views"])

@router.get("/", response_class=HTMLResponse)
def index():
    return RedirectResponse(url="/pos")

@router.get("/pos", response_class=HTMLResponse)
def pos_view(request: Request, db: Session = Depends(get_db)):
    tables = db.query(Table).order_by(Table.id).all()
    categories = db.query(Category).order_by(Category.display_order).all()
    menus = db.query(Menu).filter(Menu.is_available == True).order_by(Menu.name).all()
    active_orders = (
        db.query(Order)
        .filter(Order.status == "active")
        .order_by(Order.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="pos/index.html",
        context={
            "app_name": APP_NAME,
            "tables": tables,
            "categories": categories,
            "menus": menus,
            "active_orders": active_orders,
            "tax_rate": TAX_RATE
        }
    )

@router.get("/waiter", response_class=HTMLResponse)
def waiter_view(request: Request, db: Session = Depends(get_db)):
    tables = db.query(Table).order_by(Table.id).all()
    categories = db.query(Category).order_by(Category.display_order).all()
    menus = db.query(Menu).filter(Menu.is_available == True).order_by(Menu.name).all()

    return templates.TemplateResponse(
        request=request,
        name="waiter/index.html",
        context={
            "app_name": APP_NAME,
            "tables": tables,
            "categories": categories,
            "menus": menus
        }
    )

@router.get("/kitchen", response_class=HTMLResponse)
def kitchen_view(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="kitchen/index.html",
        context={
            "app_name": APP_NAME
        }
    )

@router.get("/admin/menu", response_class=HTMLResponse)
def admin_menu_view(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.display_order).all()
    menus = db.query(Menu).order_by(Menu.category_id, Menu.name).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/menu.html",
        context={
            "app_name": APP_NAME,
            "categories": categories,
            "menus": menus
        }
    )

@router.get("/admin/reports", response_class=HTMLResponse)
def admin_reports_view(request: Request, db: Session = Depends(get_db)):
    # Rekap pendapatan hari ini
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_payments = (
        db.query(Payment)
        .filter(Payment.payment_time >= today_start)
        .all()
    )
    today_income = sum(p.final_amount for p in today_payments)
    today_count = len(today_payments)

    # Riwayat 20 transaksi terakhir
    recent_payments = (
        db.query(Payment)
        .order_by(Payment.payment_time.desc())
        .limit(20)
        .all()
    )

    # Menu terlaris
    top_menus = (
        db.query(Menu.name, func.sum(OrderItem.quantity).label("total_qty"))
        .join(OrderItem, OrderItem.menu_id == Menu.id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.status == "completed")
        .group_by(Menu.id, Menu.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="admin/reports.html",
        context={
            "app_name": APP_NAME,
            "today_income": today_income,
            "today_count": today_count,
            "recent_payments": recent_payments,
            "top_menus": top_menus
        }
    )
