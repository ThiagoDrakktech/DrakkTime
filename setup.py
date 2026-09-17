"""
Script para gerar um executável do DrakkTime para Windows.
Requer: pip install pyinstaller
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def build_executable():
    """Constrói um executável usando PyInstaller."""
    import subprocess

    print("🔨 Compilando DrakkTime...")
    print("Certifique-se que PyInstaller está instalado: pip install pyinstaller\n")

    spec_content = """# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['drakktime/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PySimpleGUI'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DrakkTime',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""

    # Salvar spec
    with open("drakktime.spec", "w") as f:
        f.write(spec_content)

    # Executar PyInstaller
    result = subprocess.run(
        ["pyinstaller", "--onefile", "--windowed", "--name", "DrakkTime", "drakktime/__main__.py"],
        cwd=str(project_root),
    )

    if result.returncode == 0:
        print("\n✅ Executável criado com sucesso!")
        print(f"📦 Localização: {project_root / 'dist' / 'DrakkTime.exe'}")
    else:
        print("\n❌ Erro ao compilar. Verifique as dependências.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build_executable()
    else:
        print("🕐 DrakkTime - Sistema de Controle de Horas Extras")
        print("\nUsos:")
        print("  python setup.py build    - Compilar executável para Windows")
        print("  python -m drakktime      - Executar diretamente")
