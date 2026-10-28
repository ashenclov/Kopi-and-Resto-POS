import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'resto_pos.db'}"

APP_NAME = "Kopi & Resto POS"
APP_DESCRIPTION = "Sistem Kasir Modern Kafe & Restoran"

# Biaya tambahan (dapat diubah sesuai kebutuhan bisnis)
TAX_RATE = 0.10  # Pajak Resto 10% (PB1) - dapat diset 0.0 jika tidak dipakai
SERVICE_CHARGE_RATE = 0.0  # Service charge (opsional)
