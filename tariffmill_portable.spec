# -*- mode: python ; coding: utf-8 -*-
"""
TariffMill PyInstaller Spec File - Portable/Mobile Version
Build command: pyinstaller tariffmill_portable.spec

This creates a portable version that stores data in the application directory
instead of user's AppData, making it suitable for USB drives and portable use.
"""

import os
import sys

block_cipher = None

# Get the absolute path to the Tariffmill directory
tariffmill_dir = os.path.join(os.path.dirname(os.path.abspath(SPEC)), 'Tariffmill')

# Find Python DLLs to include
python_dir = os.path.dirname(sys.executable)
python_dlls = []
for dll_name in ['python3.dll', 'python312.dll', 'vcruntime140.dll', 'vcruntime140_1.dll']:
    dll_path = os.path.join(python_dir, dll_name)
    if os.path.exists(dll_path):
        python_dlls.append((dll_path, '.'))

# Analysis configuration
a = Analysis(
    [os.path.join(tariffmill_dir, 'tariffmill.py')],
    pathex=[tariffmill_dir],
    binaries=python_dlls,
    datas=[
        # Resources
        (os.path.join(tariffmill_dir, 'Resources', 'icon.ico'), 'Resources'),
        (os.path.join(tariffmill_dir, 'Resources', 'icon_portable.ico'), 'Resources'),
        (os.path.join(tariffmill_dir, 'Resources', 'tariffmill.db'), 'Resources'),
        (os.path.join(tariffmill_dir, 'Resources', 'tariffmill_logo_small.svg'), 'Resources'),
        (os.path.join(tariffmill_dir, 'Resources', 'tariffmill_logo_small_dark.svg'), 'Resources'),
        (os.path.join(tariffmill_dir, 'Resources', 'tariffmill_icon_hybrid_2.svg'), 'Resources'),
        # Reference files
        (os.path.join(tariffmill_dir, 'Resources', 'References', 'hts.db'), 'Resources/References'),
        (os.path.join(tariffmill_dir, 'Resources', 'References', 'CBP_232_tariffs.xlsx'), 'Resources/References'),
        (os.path.join(tariffmill_dir, 'Resources', 'References', 'SEC232.txt'), 'Resources/References'),
        (os.path.join(tariffmill_dir, 'Resources', 'References', 'Attachment 2_Auto Parts HTS List.txt'), 'Resources/References'),
        # Templates directory
        (os.path.join(tariffmill_dir, 'templates'), 'templates'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtSvg',
        'pandas',
        'pandas._libs',
        'pandas._libs.tslibs',
        'numpy',
        'openpyxl',
        'openpyxl.styles',
        'pdfplumber',
        'PIL',
        'PIL.Image',
        'requests',
        'sqlite3',
        'json',
        'csv',
        'xml.etree.ElementTree',
        'xml.dom.minidom',
        'configparser',
        'hashlib',
        'threading',
        'concurrent.futures',
        'dataclasses',
        'typing',
        'pathlib',
        'tempfile',
        'webbrowser',
        'socket',
        'getpass',
        # AI providers (Anthropic only)
        'anthropic',
        'anthropic._client',
        'anthropic._base_client',
        'anthropic.resources',
        'anthropic.types',
        'httpx',
        'httpcore',
        'anyio',
        'sniffio',
        'h11',
        'certifi',
        'httpx._transports',
        'httpx._transports.default',
        # TariffMill modules
        'ai_providers',
        'ai_agent_core',
        'ai_agent_tools',
        'ai_agent_ui',
        'ai_agent_integration',
        'template_builder',
        'template_wizard',
        'ocrmill_processor',
        'ocrmill_database',
        'ocrmill_worker',
        'version',
        # Templates
        'templates',
        'templates.base_template',
        'templates.bill_of_lading',
        'templates.lacey_act_form',
        'templates.sample_template',
        'templates.us_customsppq_plant_protection_and_quarantine',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ archive
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Executable - Portable version
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TariffMill_Portable',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(tariffmill_dir, 'Resources', 'icon_portable.ico'),
)

# Collect files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TariffMill_Portable',
)
