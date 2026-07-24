#!/usr/bin/env python3
# PYTHON TO .SO ENCRYPTER - TERMUX EDITION 😈
# Pake clang (bawaan Termux)
#ai generate

import os
import sys
import shutil
import subprocess
import glob
from pathlib import Path

OUTPUT_DIR = "build_so"

def check_dependencies():
    # Cek clang (bawaan Termux)
    try:
        subprocess.run(["clang", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[✓] Clang OK (compiler bawaan Termux)")
    except FileNotFoundError:
        print("[!] Clang belum terinstall! Install: pkg install clang")
        return False
    
    try:
        import Cython
        print(f"[✓] Cython {Cython.__version__} OK")
    except ImportError:
        print("[!] Cython belum terinstall! Install: pip install cython")
        return False
    
    return True

def create_setup(script_name):
    setup_content = f'''
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="{Path(script_name).stem}",
    ext_modules=cythonize(
        "{script_name}",
        compiler_directives={{
            "language_level": "3",
            "boundscheck": False,
            "wraparound": False,
        }}
    ),
)
'''
    with open("setup_temp.py", "w") as f:
        f.write(setup_content)
    print("[✓] setup.py dibuat")

def compile_so(script_file):
    print(f"\n[+] Compiling {script_file}...")
    
    # Buat file setup yang langsung ngarah ke clang
    env = os.environ.copy()
    env["CC"] = "clang"
    env["CXX"] = "clang++"
    
    cmd = [
        sys.executable,
        "setup_temp.py",
        "build_ext",
        "--inplace",
        "--force"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    if result.returncode != 0:
        print("[✗] Compile gagal!")
        print(result.stderr)
        return None
    
    # Cari file .so
    so_files = glob.glob("*.so")
    if not so_files:
        print("[!] Tidak ada .so yang dihasilkan")
        return None
    
    print("\n[+] File .so yang dihasilkan:")
    for so in so_files:
        size = os.path.getsize(so) / 1024
        print(f"    - {so} ({size:.2f} KB)")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for so in so_files:
        dest = Path(OUTPUT_DIR) / so
        shutil.move(so, str(dest))
        print(f"[✓] Dipindahkan ke: {dest}")
    
    # Bersihkan
    for c_file in glob.glob("*.c"):
        os.remove(c_file)
    shutil.rmtree("build", ignore_errors=True)
    os.remove("setup_temp.py")
    
    return so_files

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(r"""
  ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
  ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
  █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
  ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
  ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║        ██║   
  ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
    """)
    print("PYTHON TO .SO - TERMUX EDITION")
    print("="*60)
    print("[!] Pake clang (compiler bawaan Termux)")
    print("[!] Install: pkg install clang && pip install cython\n")
    
    if not check_dependencies():
        return
    
    script = input("[?] Path script Python: ").strip()
    if not script or not os.path.exists(script):
        print("[!] File tidak ditemukan!")
        return
    
    confirm = input(f"[?] Enkripsi {script}? (y/n): ").strip().lower()
    if confirm != 'y':
        return
    
    create_setup(script)
    so_files = compile_so(script)
    
    if so_files:
        print("\n" + "="*60)
        print("[✓] ENKRIPSI BERHASIL!")
        print(f"[+] File .so ada di: {OUTPUT_DIR}/")
        for so in so_files:
            print(f"    - {OUTPUT_DIR}/{so}")
        print("\n[!] Cara pake:")
        print(f"    from {Path(so_files[0]).stem} import *")
    else:
        print("\n[✗] ENKRIPSI GAGAL!")

if __name__ == "__main__":
    main()