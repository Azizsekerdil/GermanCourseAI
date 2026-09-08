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
        # Attribution obligation of the bundled MIT/BSD/HPND components:
        # the notices must travel with the binary, not only with the repository.
        (str(root / "LICENSE"), "."),
        (str(root / "THIRD_PARTY_NOTICES.md"), "."),
    ],
    hiddenimports=["pypdf", "gca.secrets", "gca.dictionary", "gca.dict_data", "gca.tabs.dictionary"],
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
