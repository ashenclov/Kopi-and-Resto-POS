import socket
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, APP_DESCRIPTION
from app.database import engine, Base, SessionLocal
from app.services.seed_data import seed_initial_data
from app.routers import views, api

# Inisialisasi Tabel Database
Base.metadata.create_all(bind=engine)

# Inisialisasi Data Awal (Seeder)
with SessionLocal() as db:
    seed_initial_data(db)

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version="1.0.0"
)

# Static files
static_dir = Path(__file__).resolve().parent / "app" / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Registrasi Router
app.include_router(views.router)
app.include_router(api.router)

def get_local_ip() -> str:
    """Mendapatkan alamat IP lokal komputer di jaringan WiFi toko."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 8000
    print("=" * 60)
    print(f"🚀 {APP_NAME} Siap Digunakan!")
    print("=" * 60)
    print(f"💻 Akses Komputer Kasir : http://localhost:{port}/pos")
    print(f"📱 Akses HP/Tablet Waiter: http://{local_ip}:{port}/waiter")
    print(f"🍳 Akses Layar Dapur (KDS): http://{local_ip}:{port}/kitchen")
    print(f"📊 Akses Laporan & Menu  : http://localhost:{port}/admin/reports")
    print("=" * 60)
    print("Tekan CTRL+C untuk menghentikan server.")
    print("=" * 60)

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
