# ☕ Kopi & Resto POS - Aplikasi Kasir F&B Berbasis Python

Aplikasi Point of Sale (Kasir) modern khusus F&B (Kafe & Restoran) yang dibangun menggunakan **Python (FastAPI)**, **Tailwind CSS**, dan **SQLite**. 

Aplikasi ini dapat diakses secara bersamaan (multi-device) dalam satu jaringan WiFi lokal tanpa perlu koneksi internet:
- **PC Kasir**: Memproses pembayaran, diskon, kembalian, dan cetak struk thermal (58mm/80mm).
- **HP / Tablet Waiter**: Pelayan memilih nomor meja, memilih menu, mencatat request khusus ("Less sugar", "Pedas"), dan kirim order.
- **Layar Dapur (Kitchen Display System)**: Memantau tiket pesanan masuk secara real-time dan update status pengerjaan.
- **Admin**: Kelola katalog menu, status ketersediaan, dan pantau omzet & menu terlaris.

---

## 🛠️ Persyaratan Sistem
- Python 3.10 atau versi lebih baru
- Windows 10/11 / macOS / Linux
- Browser modern (Chrome, Edge, Safari, Firefox)

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Install Dependensi
Buka Terminal / Command Prompt di folder proyek ini:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python main.py
```
atau klik dua kali file **`start.bat`** di Windows.

Saat server aktif, URL akses akan ditampilkan di terminal:
- **Layar Kasir:** `http://localhost:8000/pos`
- **Order Waiter (HP/Tablet):** `http://<IP-LOKAL>:8000/waiter`
- **Layar Dapur:** `http://<IP-LOKAL>:8000/kitchen`
- **Manajemen Menu:** `http://localhost:8000/admin/menu`
- **Laporan Penjualan:** `http://localhost:8000/admin/reports`

---

## 📂 Struktur Proyek
```
kasir/
├── app/
│   ├── config.py              # Konfigurasi nama resto, pajak & database
│   ├── database.py            # SQLite Engine & Session
│   ├── models/                # Tabel: Table, Category, Menu, Order, Payment
│   ├── routers/
│   │   ├── api.py             # REST API untuk interaksi AJAX cepat
│   │   └── views.py           # Render template halaman HTML
│   ├── services/
│   │   ├── order_service.py   # Logika bisnis checkout & kalkulasi
│   │   └── seed_data.py       # Data demo awal (10 meja, kategori & menu)
│   └── templates/             # Tampilan responsif Tailwind CSS
│       ├── base.html          # Layout universal & format struk thermal
│       ├── pos/               # Layar kasir & pembayaran
│       ├── waiter/            # Layar pemesanan pelayan (mobile friendly)
│       ├── kitchen/           # Kitchen Display System (KDS)
│       └── admin/             # Kelola menu & laporan transaksi
├── data/
│   └── resto_pos.db           # File database SQLite lokal
├── main.py                    # Entry point server FastAPI
├── requirements.txt
├── start.bat                  # Shortcut 1-klik untuk Windows
└── README.md
```

---

## 🖨️ Cetak Struk Belanja
Format struk dirancang otomatis menyesuaikan printer thermal **58mm** dan **80mm**. Struk langsung dapat dicetak melalui tombol cetak di browser (`window.print()`).
