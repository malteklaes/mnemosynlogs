# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\mnemosynlogs\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('src/mnemosynlogs/gui/assets', 'mnemosynlogs/gui/assets'), ('src/mnemosynlogs/config/defaults.json', 'mnemosynlogs/config'), ('src/mnemosynlogs/data', 'mnemosynlogs/data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MnemoSynLogs',
    debug=False,
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
    icon=['src\\mnemosynlogs\\gui\\assets\\icon.ico'],
)
