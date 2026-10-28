import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Di Vercel Serverless, filesystem bersifat read-only kecuali folder /tmp
if os.environ.get("VERCEL"):
    DATA_DIR = Path("/tmp")
else:
    DATA_DIR = BASE_DIR / "data"
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        DATA_DIR = Path("/tmp")

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR / 'resto_pos.db'}")

APP_NAME = "Kopi & Resto POS"
APP_DESCRIPTION = "Sistem Kasir Modern Kafe & Restoran"

# Biaya tambahan (dapat diubah sesuai kebutuhan bisnis)
TAX_RATE = 0.10  # Pajak Resto 10% (PB1) - dapat diset 0.0 jika tidak dipakai
SERVICE_CHARGE_RATE = 0.0  # Service charge (opsional)
