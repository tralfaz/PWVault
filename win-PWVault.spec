# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\pwvuiapp.py'],
    pathex=[],
    binaries=[],
    datas=[('../assets/copy-button-icon.png',    'assets'),
            ('../assets/edit-button-icon.png',   'assets'),
            ('../assets/padlock-icon.png',       'assets'),
            ('../assets/eye-open-yellow.svg',    'assets'),
            ('../assets/eye-blocked-yellow.svg', 'assets'),
            ('../assets/search-icon-yellow.svg', 'assets')
           ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PWVault',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    icon="../assets/vault-icon.ico",
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PWVault',
)
