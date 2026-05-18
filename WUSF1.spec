# WUSF1.spec
import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Recoger datos necesarios de fastf1
fastf1_data = collect_data_files('fastf1')

a = Analysis( 
    ['main.py'], 
    pathex=[os.path.join(SPECPATH, 'src')], # Where to find modules
    binaries=[],
    datas=[*fastf1_data,         # Includes fastf1 data files
    ('logo.ico', '.')],                   
    hiddenimports=[ 
    'ui', 
    'plots', 
    'themes', 
    'state', 
    'data_loader',
    'fastf1',
    'fastf1.plotting', 
    'scipy.interpolate',
    'scipy._lib.messagestream',
    'numpy', 
    'dearpygui',
    'dearpygui.dearpygui',
    ], 
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WUSF1',
    debug=False,
    icon='logo.ico',
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)