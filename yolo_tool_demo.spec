# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['yolo_tool_demo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['accord_txt_select_img', 'batch_modify_txt_class', 'check_and_create_empty_txt', 'read_videos','accord_yololabel_crop_image_and_joint', 'batch_modify_box_class','build_dataset'],
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
    name='yolo_tool_demo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
