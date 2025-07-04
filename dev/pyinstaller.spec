# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Add all necessary hidden imports
hidden_imports = [
    'flask', 'werkzeug', 'jinja2', 'itsdangerous', 'click',
    'flask.cli', 'flask.json', 'flask.templating',
    'subprocess', 'logging', 'time', 'threading', 'webbrowser'
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[
        ('video_converter/backend/bin/ffmpeg.exe', 'bin')
    ],
    datas=[
        ('templates/*.html', 'templates'),
        ('static/*', 'static'),
        ('video_converter/backend/uploads', 'uploads'),
        ('video_converter/backend/converted', 'converted')
    ],
    hiddenimports=hidden_imports,
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
    name='video_converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'  # Add if you have an icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='video_converter',
)