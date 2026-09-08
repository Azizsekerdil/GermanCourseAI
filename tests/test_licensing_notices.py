"""Guards the licensing paperwork: the notices must stay factual and must ship with the binaries.

These are the exact claims an OSS-compliance scan or a downstream redistributor checks, so each
one is pinned to something the repository can verify on its own.
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTICES = ROOT / "THIRD_PARTY_NOTICES.md"
SPEC = ROOT / "GermanCourseAI.spec"
BUILD_BAT = ROOT / "build.bat"
BUILD_MACOS = ROOT / "build_macos.sh"

# Every file that repeats the copyleft claim for a reader; each must carry the libgfortran
# qualification rather than an unconditional "no GPL library is bundled".
CLAIM_FILES = [
    NOTICES,
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs" / "KULLANIM_KILAVUZU.md",
    ROOT / "docs" / "USER_GUIDE.md",
]

# Phrasings that were factually wrong: libgfortran (GPL-3.0-or-later WITH GCC-exception-3.1) is
# statically linked into the OpenBLAS DLL that NumPy contributes to the Windows executable.
FORBIDDEN_ABSOLUTES = [
    "No GPL, LGPL, AGPL or other copyleft library is linked into or bundled",
    "No GPL, LGPL or AGPL library is linked into or bundled",
    "No GPL, LGPL or AGPL library is bundled",
    "GPL, LGPL ya da AGPL lisanslı hiçbir kütüphane bulunmaz",
    "GPL, LGPL veya AGPL lisanslı hiçbir kütüphane yoktur",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unwrapped(text: str) -> str:
    """Collapse whitespace so a claim split across wrapped lines is still matched."""
    return " ".join(text.split())


@pytest.mark.parametrize("path", CLAIM_FILES, ids=lambda p: p.name)
def test_copyleft_claim_is_qualified(path: Path) -> None:
    text = read(path)
    flat = unwrapped(text)
    for phrase in FORBIDDEN_ABSOLUTES:
        assert unwrapped(phrase) not in flat, f"{path.name} repeats the unqualified claim: {phrase!r}"
    assert "GCC Runtime Library Exception" in text or "GCC-exception-3.1" in text, (
        f"{path.name} states a copyleft conclusion without naming the libgfortran exception it rests on"
    )


def test_notices_name_libgfortran_and_its_exception() -> None:
    text = read(NOTICES)
    assert "libgfortran" in text
    assert "GPL-3.0-or-later" in text and "GCC-exception-3.1" in text
    # The OpenBLAS row must not claim a bare BSD-3-Clause any more.
    openblas_row = next(line for line in text.splitlines() if "libscipy_openblas64_" in line)
    assert "GCC Fortran runtime" in openblas_row and "GCC-exception-3.1" in openblas_row


@pytest.mark.parametrize("component", ["cffi", "typing_extensions"])
def test_components_really_in_the_windows_binary_are_listed(component: str) -> None:
    """Both are collected into dist/GermanCourseAI.exe; cffi is MIT and needs its notice kept."""
    assert component in read(NOTICES)


def test_pyinstaller_runtime_hooks_declared_apache() -> None:
    """rthooks are embedded in the frozen exe and are Apache-2.0, not GPL-with-exception."""
    text = read(NOTICES)
    assert "pyi_rth_cryptography_openssl" in text
    hook_section = text[text.index("## 4. Build-time tools"):text.index("## 5. Obligations")]
    assert "Apache-2.0" in hook_section
    assert "## 4. Build-time tools (not part of the application)" not in text


def test_brotli_not_attributed_to_a_module_that_is_absent() -> None:
    """Brotli reaches Pillow only through _imagingft, which is not in the build."""
    text = read(NOTICES)
    disclaimer = "FreeType, HarfBuzz and Brotli are **not** part of this build"
    assert disclaimer in text
    enumeration = text[text.index("Pillow's C extensions statically link"): text.index(disclaimer)]
    assert "Brotli" not in enumeration, "Brotli is listed as statically linked, but _imagingft is absent"


def test_notices_ship_with_every_binary() -> None:
    """Section 5 promises the notices travel with the binaries; the build scripts must deliver."""
    spec = read(SPEC)
    assert '(str(root / "LICENSE"), ".")' in spec
    assert '(str(root / "THIRD_PARTY_NOTICES.md"), ".")' in spec

    macos = read(BUILD_MACOS)
    assert "for file in LICENSE THIRD_PARTY_NOTICES.md" in macos
    assert '--add-data "$PROJECT_ROOT/$file:."' in macos

    bat = read(BUILD_BAT)
    assert "GermanCourseAI-Windows.zip" in bat
    for name in ("GermanCourseAI.exe", "LICENSE", "THIRD_PARTY_NOTICES.md"):
        assert f'"%CD%\\{name}"' in bat or f'"%CD%\\dist\\{name}"' in bat, name


def test_macos_build_uses_its_own_virtualenv() -> None:
    """The notices claim the macOS build cannot inherit the developer's site-packages."""
    macos = read(BUILD_MACOS)
    assert "-m venv build/macos/venv" in macos
    assert 'PYTHON_BIN="$PROJECT_ROOT/build/macos/venv/bin/python"' in macos
    venv_at = macos.index("-m venv build/macos/venv")
    assert macos.index("pip install -r requirements.txt") > venv_at, "pip runs outside the venv"
    assert macos.index("rm -rf build/macos") < venv_at, "the venv is created then deleted"


def test_section_two_maps_to_the_macos_bundle_too() -> None:
    """Section 2 covers the .app as well, so it must name the macOS artifacts."""
    text = read(NOTICES)
    for name in ("Python.framework", "libtcl8.6.dylib", "libcrypto.3.dylib", "cpython-311-darwin.so"):
        assert name in text, f"section 2 never mentions the macOS artifact {name}"
    assert "`libffi` is **not** bundled on macOS" in text


def test_guide_pdfs_match_their_markdown_sources() -> None:
    """The tracked PDFs are release artifacts; a stale one ships a guide with no licence section."""
    pypdf = pytest.importorskip("pypdf")
    for stem, heading in [("USER_GUIDE", "12. License"), ("KULLANIM_KILAVUZU", "12. Lisans")]:
        md = ROOT / "docs" / f"{stem}.md"
        pdf = ROOT / "docs" / f"{stem}.pdf"
        assert f"## {heading}" in read(md)
        reader = pypdf.PdfReader(str(pdf))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        assert heading in text, f"{pdf.name} is stale: regenerate with `python docs/build_guides.py`"
        assert "THIRD_PARTY_NOTICES.md" in text


def test_no_personal_paths_in_tracked_sources() -> None:
    """A repository about to go public must not leak the author's profile path or an internal tool URL."""
    # Split so this file does not match its own needles.
    user_dir = "C:" + "/Users/" + "azizs"
    needles = [user_dir, user_dir.replace("/", "\\"), "codex-" + "runtimes"]
    checked = 0
    skip_dirs = {".git", "build", "dist", "tmp", "__pycache__", ".pytest_cache", ".ui-smoke"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".mjs", ".md", ".txt", ".bat", ".sh", ".spec", ".yml"}:
            continue
        if any(part in skip_dirs for part in path.relative_to(ROOT).parts):
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        for needle in needles:
            assert needle not in content, f"{path.relative_to(ROOT)} contains {needle!r}"
        checked += 1
    assert checked > 20, "the sweep found almost no files; the walk is broken"
