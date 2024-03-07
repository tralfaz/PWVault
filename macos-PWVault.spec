# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pwvuiapp.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/copy-black.svg',         'assets'),
           ('assets/copy-yellow.svg',        'assets'),
           ('assets/edit-red.svg',           'assets'),
           ('assets/padlock-icon.png',       'assets'),
           ('assets/eye-open-black.svg',     'assets'),
           ('assets/eye-blocked-black.svg',  'assets'),
           ('assets/eye-open-yellow.svg',    'assets'),
           ('assets/eye-blocked-yellow.svg', 'assets'),
           ('assets/less-black.svg',         'assets'),
           ('assets/less-yellow.svg',        'assets'),
           ('assets/more-black.svg',         'assets'),
           ('assets/more-yellow.svg',        'assets'),
           ('assets/search-icon-yellow.svg', 'assets')
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
app = BUNDLE(
    coll,
    name='PWVault.app',
    icon='assets/pwvault-app.icns',
    bundle_identifier='com.midoma.pyapps.pwvault',
    info_plist={
        'CFBundleURLTypes': [{
            'CFBundleURLName': 'PWVaultUrlSchema',
            'CFBundleTypeRole': 'Viewer',
            'CFBundleURLSchemes': ['pwvault-url', ],
        }],
        'CFBundleDocumentTypes': [{
            'CFBundleTypeName': 'PWVaultFileType',
            'CFBundleTypeExtensions': ['pwv', ],
            'CFBundleTypeRole': "Viewer",
            'CFBundleTypeIconFile': 'pwvault-doc.icns',
        }],
    }
)
