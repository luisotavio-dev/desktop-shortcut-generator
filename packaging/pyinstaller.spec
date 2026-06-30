# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Desktop Shortcut Generator Linux builds."""

from pathlib import Path

block_cipher = None
root = Path(SPECPATH).resolve().parent

a = Analysis(
    [str(root / "desktop_shortcut_generator" / "main.py")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (
            str(root / "desktop_shortcut_generator" / "i18n" / "locales"),
            "desktop_shortcut_generator/i18n/locales",
        ),
        (
            str(root / "desktop_shortcut_generator" / "assets"),
            "desktop_shortcut_generator/assets",
        ),
    ],
    hiddenimports=[
        "desktop_shortcut_generator",
        "desktop_shortcut_generator.config",
        "desktop_shortcut_generator.config.settings",
        "desktop_shortcut_generator.domain",
        "desktop_shortcut_generator.domain.entities",
        "desktop_shortcut_generator.domain.exceptions",
        "desktop_shortcut_generator.use_cases",
        "desktop_shortcut_generator.use_cases.create_shortcut",
        "desktop_shortcut_generator.infrastructure",
        "desktop_shortcut_generator.infrastructure.file_writer",
        "desktop_shortcut_generator.infrastructure.xdg_paths",
        "desktop_shortcut_generator.infrastructure.desktop_trust",
        "desktop_shortcut_generator.presentation",
        "desktop_shortcut_generator.presentation.main_window",
        "desktop_shortcut_generator.presentation.components",
        "desktop_shortcut_generator.i18n",
        "desktop_shortcut_generator.i18n.translator",
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
    [],
    exclude_binaries=True,
    name="desktop-shortcut-generator",
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="desktop-shortcut-generator",
)
