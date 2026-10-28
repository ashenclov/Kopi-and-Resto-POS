import sys
from pathlib import Path

# Tambahkan root project ke sys.path agar import 'main' dan 'app' bisa ditemukan
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
