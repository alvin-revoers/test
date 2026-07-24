import importlib
import sys
from pathlib import Path

# Cari file .so di folder saat ini
so_files = list(Path(".").glob("*.so"))
if not so_files:
    print("[!] Tidak ada file .so")
    sys.exit(1)

# Ambil file .so pertama
so = so_files[0]
name = so.stem.split(".cpython")[0]

# Import dan jalankan
mod = importlib.import_module(name)
if hasattr(mod, "main"):
    mod.main()
else:
    print("[!] Fungsi main() tidak ditemukan")
    print("[!] Fungsi:", [f for f in dir(mod) if not f.startswith("_")])