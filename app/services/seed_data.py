from sqlalchemy.orm import Session
from app.models.models import Table, Category, Menu

def seed_initial_data(db: Session):
    # Cek apakah sudah ada data kategori
    if db.query(Category).first():
        return

    # 1. Seeder Meja
    tables_data = [
        {"table_number": "Meja 01", "capacity": 2},
        {"table_number": "Meja 02", "capacity": 2},
        {"table_number": "Meja 03", "capacity": 4},
        {"table_number": "Meja 04", "capacity": 4},
        {"table_number": "Meja 05", "capacity": 4},
        {"table_number": "Meja 06", "capacity": 6},
        {"table_number": "Meja 07", "capacity": 6},
        {"table_number": "Meja VIP 1", "capacity": 8},
        {"table_number": "Bar 01", "capacity": 1},
        {"table_number": "Bar 02", "capacity": 1},
    ]
    for t in tables_data:
        db.add(Table(table_number=t["table_number"], capacity=t["capacity"], status="available"))

    # 2. Seeder Kategori
    cat_food = Category(name="Makanan Utama", icon="utensils", display_order=1)
    cat_coffee = Category(name="Kopi & Espresso", icon="coffee", display_order=2)
    cat_non_coffee = Category(name="Minuman Segar", icon="glass-water", display_order=3)
    cat_snack = Category(name="Cemilan & Snack", icon="cookie", display_order=4)
    cat_dessert = Category(name="Dessert", icon="ice-cream", display_order=5)

    db.add_all([cat_food, cat_coffee, cat_non_coffee, cat_snack, cat_dessert])
    db.flush()  # dapatkan ID kategori

    # 3. Seeder Menu
    menus_data = [
        # Makanan Utama
        {"cat_id": cat_food.id, "name": "Nasi Goreng Spesial Resto", "desc": "Nasi goreng bumbu rempah dengan telur mata sapi, sate ayam, dan kerupuk", "price": 28000},
        {"cat_id": cat_food.id, "name": "Mie Goreng Jawa", "desc": "Mie telur kenyal dengan suwiran ayam, bakso, dan sayuran segar", "price": 25000},
        {"cat_id": cat_food.id, "name": "Ayam Bakar Madu + Nasi", "desc": "Ayam bakar manis gurih lengkap dengan nasi pulen, sambal terasi dan lalapan", "price": 32000},
        {"cat_id": cat_food.id, "name": "Rice Bowl Beef Teriyaki", "desc": "Daging sapi iris saus teriyaki khas jepang diatas nasi hangat dengan taburan wijen", "price": 35000},
        {"cat_id": cat_food.id, "name": "Spaghetti Bolognese", "desc": "Pasta spaghetti dengan saus daging cincang tomat segar dan keju parmesan", "price": 30000},

        # Kopi & Espresso
        {"cat_id": cat_coffee.id, "name": "Kopi Susu Gula Aren", "desc": "Espresso blend arabika-robusta dengan fresh milk dan gula aren asli", "price": 20000},
        {"cat_id": cat_coffee.id, "name": "Caffe Latte", "desc": "Espresso halus berpadu susu steamed lembut", "price": 24000},
        {"cat_id": cat_coffee.id, "name": "Americano / Long Black", "desc": "Espresso ganda dengan air mineral segar (bisa panas / dingin)", "price": 18000},
        {"cat_id": cat_coffee.id, "name": "Caramel Macchiato", "desc": "Vanilla milk dengan espresso shot dan drizzle saus karamel lezat", "price": 26000},

        # Minuman Segar
        {"cat_id": cat_non_coffee.id, "name": "Lemon Tea Dingin", "desc": "Teh melati pilihan dengan perasan lemon segar asli", "price": 15000},
        {"cat_id": cat_non_coffee.id, "name": "Matcha Green Tea Latte", "desc": "Pure uji matcha jepang dengan susu segar", "price": 25000},
        {"cat_id": cat_non_coffee.id, "name": "Lychee Yakult Breeze", "desc": "Kombinasi probiotik yakult, sirup leci, dan buah leci asli", "price": 22000},
        {"cat_id": cat_non_coffee.id, "name": "Air Mineral 600ml", "desc": "Air mineral botol dingin / suhu ruang", "price": 6000},

        # Cemilan & Snack
        {"cat_id": cat_snack.id, "name": "French Fries Original", "desc": "Kentang goreng renyah dengan saus sambal dan mayonaise", "price": 18000},
        {"cat_id": cat_snack.id, "name": "Tahu Crispy Cabe Garam", "desc": "Tahu sutra goreng garing dengan taburan bawang putih, cabai, dan garam", "price": 16000},
        {"cat_id": cat_snack.id, "name": "Platter Mix Snack", "desc": "Kombinasi sosis, nugget, dan kentang goreng porsi sharing", "price": 30000},

        # Dessert
        {"cat_id": cat_dessert.id, "name": "Pisang Goreng Keju Cokelat", "desc": "Pisang raja manis goreng tepung dengan topping cokelat parut dan keju cheddar", "price": 20000},
        {"cat_id": cat_dessert.id, "name": "Croffle Brown Sugar", "desc": "Croissant waffle hangat garing berlapis brown sugar", "price": 22000},
    ]

    for m in menus_data:
        db.add(Menu(
            category_id=m["cat_id"],
            name=m["name"],
            description=m["desc"],
            price=m["price"],
            is_available=True
        ))

    db.commit()
