"""Guards the licensing paperwork: the notices must stay factual and must ship with the binaries.

These are the exact claims an OSS-compliance scan or a downstream redistributor checks, so each
one is pinned to something the repository can verify on its own. Since 1.3.0 both packages are
built in a dedicated virtual environment, so the claims are checked against what the frozen build
really contains rather than trusted.
"""
from __future__ import annotations

import ast
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTICES = ROOT / "THIRD_PARTY_NOTICES.md"
SPEC = ROOT / "GermanCourseAI.spec"
BUILD_BAT = ROOT / "build.bat"
BUILD_MACOS = ROOT / "build_macos.sh"
ANALYSIS_TOC = ROOT / "build" / "GermanCourseAI" / "Analysis-00.toc"
WINDOWS_ZIP = ROOT / "dist" / "GermanCourseAI-Windows.zip"

# The only non-standard-library Python packages a clean build may contain.
EXPECTED_PACKAGES = {"gca", "pypdf"}

# Every file that repeats the copyleft claim for a reader.
CLAIM_FILES = [
    NOTICES,
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs" / "KULLANIM_KILAVUZU.md",
    ROOT / "docs" / "USER_GUIDE.md",
]

# The clean build removed NumPy, so no document may still present GPL code as being *in* a
# current binary. These are the phrasings that said exactly that.
FORBIDDEN_PRESENT_TENSE = [
    "The only GPL-licensed code present in a released binary is",
    "The only GPL-licensed code present is the libgfortran",
    "Tek GPL lisanslı parça",
]

# The conclusion each document must now state, in its own language.
ACCEPTED_CONCLUSIONS = [
    "No GPL, LGPL or AGPL library code is present",
    "no GPL, LGPL or AGPL library code is present",
    "GPL, LGPL veya AGPL lisanslı hiçbir kütüphane kodu bulunmaz",
    "No copyleft library is present in the released binaries",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unwrapped(text: str) -> str:
    """Collapse whitespace and bold markers so a claim split across lines is still matched."""
    return " ".join(text.replace("**", "").split())


def bundled_packages() -> set[str]:
    """Top-level non-stdlib Python packages in the last frozen Windows build."""
    toc = ast.literal_eval(ANALYSIS_TOC.read_text(encoding="utf-8"))
    modules = set()
    for part in toc:
        if not isinstance(part, list):
            continue
        for entry in part:
            if isinstance(entry, tuple) and len(entry) == 3 and entry[2] == "PYMODULE":
                modules.add(entry[0])
    return {name.split(".")[0] for name in modules} - set(sys.stdlib_module_names)


@pytest.mark.parametrize("path", CLAIM_FILES, ids=lambda p: p.name)
def test_copyleft_claim_matches_the_clean_build(path: Path) -> None:
    flat = unwrapped(read(path))
    for phrase in FORBIDDEN_PRESENT_TENSE:
        assert unwrapped(phrase) not in flat, (
            f"{path.name} still presents GPL code as being inside a current binary: {phrase!r}"
        )
    assert any(unwrapped(claim) in flat for claim in ACCEPTED_CONCLUSIONS), (
        f"{path.name} never states the copyleft conclusion the clean build now supports"
    )


def test_notices_record_that_libgfortran_was_removed() -> None:
    """The history matters to anyone auditing the older archives, but not as a current fact."""
    text = read(NOTICES)
    assert "libgfortran" in text and "GCC-exception-3.1" in text
    assert "libscipy_openblas64_" not in text, "the OpenBLAS row survived, but NumPy is gone"
    assert "pypdf's optional image support" not in text, "Pillow is listed as if still bundled"
    flat = unwrapped(text)
    assert "is gone together with NumPy" in flat or "is gone with NumPy" in flat


@pytest.mark.skipif(not ANALYSIS_TOC.exists(), reason="no local PyInstaller build to inspect")
def test_frozen_build_contains_only_the_declared_packages() -> None:
    """The central claim of section 3, checked against the build instead of trusted."""
    assert bundled_packages() == EXPECTED_PACKAGES


@pytest.mark.parametrize("component", sorted(EXPECTED_PACKAGES))
def test_packages_in_the_binary_are_listed(component: str) -> None:
    assert component in read(NOTICES)


def test_pyinstaller_runtime_hooks_declared_apache() -> None:
    """rthooks are embedded in the frozen exe and are Apache-2.0, not GPL-with-exception."""
    text = read(NOTICES)
    hook_section = text[text.index("## 4. Build-time tools"):text.index("## 5. Obligations")]
    for hook in ("pyi_rth_inspect", "pyi_rth__tkinter"):
        assert hook in hook_section, f"section 4 never names the embedded hook {hook}"
    assert "Apache-2.0" in hook_section
    assert "## 4. Build-time tools (not part of the application)" not in text


def test_notices_ship_with_every_binary() -> None:
    """The notices promise they travel with the binaries; the build scripts must deliver."""
    spec = read(SPEC)
    assert '(str(root / "LICENSE"), ".")' in spec
    assert '(str(root / "THIRD_PARTY_NOTICES.md"), ".")' in spec

    macos = read(BUILD_MACOS)
    assert "for file in LICENSE THIRD_PARTY_NOTICES.md" in macos
    assert '--add-data "$PROJECT_ROOT/$file:."' in macos
    # ... and next to the .app in the archive, exactly as on Windows.
    assert 'cp LICENSE THIRD_PARTY_NOTICES.md "$ZIP_STAGE/"' in macos
    assert 'ditto -c -k --sequesterRsrc "$ZIP_STAGE" "dist/GermanCourseAI-macOS.zip"' in macos

    bat = read(BUILD_BAT)
    assert "GermanCourseAI-Windows.zip" in bat
    for name in ("GermanCourseAI.exe", "LICENSE", "THIRD_PARTY_NOTICES.md"):
        assert f'"%CD%\\{name}"' in bat or f'"%CD%\\dist\\{name}"' in bat, name


@pytest.mark.skipif(not WINDOWS_ZIP.exists(), reason="no local release archive to inspect")
def test_release_archive_carries_the_notices() -> None:
    with zipfile.ZipFile(WINDOWS_ZIP) as archive:
        assert set(archive.namelist()) == {
            "GermanCourseAI.exe",
            "LICENSE",
            "THIRD_PARTY_NOTICES.md",
        }
        for info in archive.infolist():
            assert info.compress_type == zipfile.ZIP_DEFLATED


def test_windows_build_uses_a_clean_interpreter() -> None:
    """The exe must never be frozen from whatever is installed in the global interpreter."""
    bat = read(BUILD_BAT)
    assert "python -m PyInstaller" not in bat, "the build can fall back to the global interpreter"
    assert '"%PYTHON_BIN%" -m PyInstaller' in bat
    assert "-m venv" in bat
    venv_at = bat.index("-m venv")
    assert bat.index("-m pip install -r requirements.txt") > venv_at, "pip runs outside the venv"


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
