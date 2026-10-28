from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Table, Menu, Order, OrderItem, Payment
from app.config import TAX_RATE, SERVICE_CHARGE_RATE

def generate_order_number(db: Session) -> str:
    today_str = datetime.now().strftime("%Y%m%d")
    prefix = f"ORD-{today_str}-"
    # Cari order terakhir hari ini
    last_order = (
        db.query(Order)
        .filter(Order.order_number.like(f"{prefix}%"))
        .order_by(Order.id.desc())
        .first()
    )
    if last_order:
        try:
            last_seq = int(last_order.order_number.split("-")[-1])
            new_seq = last_seq + 1
        except ValueError:
            new_seq = 1
    else:
        new_seq = 1
    return f"{prefix}{new_seq:04d}"

def create_order(
    db: Session,
    order_type: str,
    customer_name: str,
    table_id: int | None,
    items: list[dict]  # [{"menu_id": int, "quantity": int, "notes": str}]
) -> Order:
    order_num = generate_order_number(db)
    new_order = Order(
        order_number=order_num,
        table_id=table_id if order_type == "dine_in" else None,
        order_type=order_type,
        customer_name=customer_name or "Pelanggan",
        status="active",
        total_amount=0.0
    )
    db.add(new_order)
    db.flush()

    total = 0.0
    for item in items:
        menu = db.query(Menu).filter(Menu.id == item["menu_id"]).first()
        if not menu:
            continue
        qty = max(1, int(item.get("quantity", 1)))
        subtotal = menu.price * qty
        total += subtotal

        order_item = OrderItem(
            order_id=new_order.id,
            menu_id=menu.id,
            quantity=qty,
            unit_price=menu.price,
            subtotal=subtotal,
            notes=item.get("notes", ""),
            status="pending"
        )
        db.add(order_item)

    new_order.total_amount = total

    # Jika dine-in dan ada meja, update status meja menjadi occupied
    if order_type == "dine_in" and table_id:
        table = db.query(Table).filter(Table.id == table_id).first()
        if table:
            table.status = "occupied"

    db.commit()
    db.refresh(new_order)
    return new_order

def process_payment(
    db: Session,
    order_id: int,
    payment_method: str,
    pay_amount: float,
    discount_amount: float = 0.0,
    cashier_name: str = "Kasir"
) -> Payment:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Pesanan tidak ditemukan")

    subtotal = order.total_amount
    discount = max(0.0, discount_amount)
    after_discount = max(0.0, subtotal - discount)
    tax = round(after_discount * TAX_RATE, 2)
    final_amount = after_discount + tax

    if pay_amount < final_amount and payment_method == "cash":
        raise ValueError(f"Uang bayar (Rp {pay_amount:,.0f}) kurang dari total tagihan (Rp {final_amount:,.0f})")

    change_amount = max(0.0, pay_amount - final_amount) if payment_method == "cash" else 0.0

    payment = Payment(
        order_id=order.id,
        payment_time=datetime.utcnow(),
        payment_method=payment_method,
        subtotal=subtotal,
        discount=discount,
        tax=tax,
        final_amount=final_amount,
        pay_amount=pay_amount if payment_method == "cash" else final_amount,
        change_amount=change_amount,
        cashier_name=cashier_name
    )
    db.add(payment)

    # Selesaikan pesanan
    order.status = "completed"

    # Kosongkan kembali meja jika dine-in
    if order.table_id:
        # Cek apakah ada order aktif lain di meja yang sama (jika tidak ada, set available)
        active_on_table = (
            db.query(Order)
            .filter(Order.table_id == order.table_id, Order.status == "active", Order.id != order.id)
            .count()
        )
        if active_on_table == 0 and order.table:
            order.table.status = "available"

    db.commit()
    db.refresh(payment)
    return payment
