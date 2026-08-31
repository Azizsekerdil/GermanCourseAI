# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

root = Path(SPEC).resolve().parent
a = Analysis(
    [str(root / "German_Course_AI.pyw")],
    pathex=[str(root)],
    binaries=[],
    datas=[
        (str(root / "assets"), "assets"),
        (str(root / "Resources"), "Resources"),
        (str(root / "grammar"), "grammar"),
    ],
    hiddenimports=["pypdf"],
    hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="GermanCourseAI",
    debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
    console=False, disable_windowed_traceback=False,
    argv_emulation=False,
    icon=str(root / "assets" / "app.ico"),
)
