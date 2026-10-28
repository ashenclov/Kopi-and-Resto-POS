from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Table, Category, Menu, Order, OrderItem, Payment
from app.services.order_service import create_order, process_payment

router = APIRouter(prefix="/api", tags=["API"])

@router.get("/tables")
def get_tables(db: Session = Depends(get_db)):
    tables = db.query(Table).order_by(Table.id).all()
    results = []
    for t in tables:
        active_order = db.query(Order).filter(Order.table_id == t.id, Order.status == "active").first()
        results.append({
            "id": t.id,
            "table_number": t.table_number,
            "capacity": t.capacity,
            "status": t.status,
            "active_order": {
                "id": active_order.id,
                "order_number": active_order.order_number,
                "customer_name": active_order.customer_name,
                "total_amount": active_order.total_amount,
                "created_at": active_order.created_at.strftime("%H:%M")
            } if active_order else None
        })
    return results

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.display_order).all()
    return [{"id": c.id, "name": c.name, "icon": c.icon} for c in categories]

@router.get("/menus")
def get_menus(category_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Menu).filter(Menu.is_available == True)
    if category_id:
        query = query.filter(Menu.category_id == category_id)
    menus = query.order_by(Menu.name).all()
    return [
        {
            "id": m.id,
            "category_id": m.category_id,
            "category_name": m.category.name if m.category else "",
            "name": m.name,
            "description": m.description,
            "price": m.price,
            "is_available": m.is_available
        }
        for m in menus
    ]

@router.post("/menus")
def create_menu(payload: dict = Body(...), db: Session = Depends(get_db)):
    category_id = payload.get("category_id")
    name = payload.get("name")
    description = payload.get("description", "")
    price = float(payload.get("price", 0.0))

    if not name or price <= 0:
        raise HTTPException(status_code=400, detail="Nama menu dan harga valid wajib diisi")

    menu = Menu(
        category_id=category_id,
        name=name,
        description=description,
        price=price,
        is_available=True
    )
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return {"success": True, "menu_id": menu.id}

@router.post("/menus/{menu_id}/toggle")
def toggle_menu_availability(menu_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu tidak ditemukan")
    
    is_available = payload.get("is_available", not menu.is_available)
    menu.is_available = is_available
    db.commit()
    return {"success": True, "menu_id": menu.id, "is_available": menu.is_available}

@router.post("/orders")
def api_create_order(payload: dict = Body(...), db: Session = Depends(get_db)):
    order_type = payload.get("order_type", "dine_in")
    customer_name = payload.get("customer_name", "Pelanggan")
    table_id = payload.get("table_id")
    items = payload.get("items", [])

    if not items:
        raise HTTPException(status_code=400, detail="Keranjang pesanan tidak boleh kosong")

    if order_type == "dine_in" and not table_id:
        raise HTTPException(status_code=400, detail="Nomor meja wajib dipilih untuk Dine-In")

    try:
        order = create_order(db, order_type, customer_name, table_id, items)
        return {
            "success": True,
            "order_id": order.id,
            "order_number": order.order_number,
            "total_amount": order.total_amount
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orders/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")

    return {
        "id": order.id,
        "order_number": order.order_number,
        "order_type": order.order_type,
        "customer_name": order.customer_name,
        "table_name": order.table.table_number if order.table else "Take Away",
        "status": order.status,
        "created_at": order.created_at.strftime("%d/%m/%Y %H:%M"),
        "total_amount": order.total_amount,
        "items": [
            {
                "id": item.id,
                "name": item.menu.name if item.menu else "Item",
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal,
                "notes": item.notes,
                "status": item.status
            }
            for item in order.items
        ]
    }

@router.post("/payments")
def api_process_payment(payload: dict = Body(...), db: Session = Depends(get_db)):
    order_id = payload.get("order_id")
    payment_method = payload.get("payment_method", "cash")
    pay_amount = float(payload.get("pay_amount", 0.0))
    discount_amount = float(payload.get("discount_amount", 0.0))
    cashier_name = payload.get("cashier_name", "Kasir")

    try:
        payment = process_payment(
            db=db,
            order_id=order_id,
            payment_method=payment_method,
            pay_amount=pay_amount,
            discount_amount=discount_amount,
            cashier_name=cashier_name
        )
        return {
            "success": True,
            "payment_id": payment.id,
            "subtotal": payment.subtotal,
            "discount": payment.discount,
            "tax": payment.tax,
            "final_amount": payment.final_amount,
            "pay_amount": payment.pay_amount,
            "change_amount": payment.change_amount,
            "receipt_number": payment.order.order_number,
            "payment_time": payment.payment_time.strftime("%d/%m/%Y %H:%M:%S")
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/kitchen/orders")
def get_kitchen_orders(db: Session = Depends(get_db)):
    active_orders = (
        db.query(Order)
        .filter(Order.status == "active")
        .order_by(Order.created_at.asc())
        .all()
    )
    result = []
    for ord in active_orders:
        pending_items = [
            {
                "id": it.id,
                "name": it.menu.name if it.menu else "",
                "quantity": it.quantity,
                "notes": it.notes,
                "status": it.status
            }
            for it in ord.items
            if it.status in ["pending", "cooking"]
        ]
        if pending_items:
            result.append({
                "order_id": ord.id,
                "order_number": ord.order_number,
                "order_type": ord.order_type,
                "table_name": ord.table.table_number if ord.table else "Take Away",
                "customer_name": ord.customer_name,
                "created_time": ord.created_at.strftime("%H:%M"),
                "items": pending_items
            })
    return result

@router.post("/kitchen/items/{item_id}/status")
def update_kitchen_item_status(item_id: int, payload: dict = Body(...), db: Session = Depends(get_db)):
    new_status = payload.get("status")
    if new_status not in ["pending", "cooking", "served"]:
        raise HTTPException(status_code=400, detail="Status tidak valid")

    item = db.query(OrderItem).filter(OrderItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item pesanan tidak ditemukan")

    item.status = new_status
    db.commit()
    return {"success": True, "item_id": item.id, "new_status": item.status}
