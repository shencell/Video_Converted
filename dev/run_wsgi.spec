# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['run_wsgi.py'],
    pathex=[],
    binaries=[],
    datas=[('video_converter/backend/bin/ffmpeg.exe', 'bin')],
    hiddenimports=['flask', 'werkzeug', 'jinja2', 'itsdangerous', 'click', 'waitress', 'waitress.server'],
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
    name='run_wsgi',
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
)
