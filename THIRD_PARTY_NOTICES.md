# Third-party notices

German Course AI itself is distributed under the MIT License (see [LICENSE](LICENSE)).
This file lists the third-party components that are used by the source tree or embedded in the
distributed binaries, together with the licence each component is actually published under.

Every licence below was read from the installed package metadata or from the component's own
licence file — none of them is guessed. The version numbers are those observed in the environment
that produced the released `1.2.1` binaries.

**No copyleft library imposes copyleft obligations on this application.** The only GPL-licensed
code present in a released binary is the libgfortran runtime that is statically linked inside
NumPy's OpenBLAS DLL on Windows; it carries the **GCC Runtime Library Exception 3.1**, which
permits redistribution under any licence — see [section 3](#3-additional-python-packages-present-in-the-released-windows-binary).
The only GPL-licensed tools involved (PyInstaller and, optionally, UPX) are build tools that carry
an explicit exception permitting the frozen application to be distributed under its own licence —
see [Build-time tools](#4-build-time-tools) below.

---

## 1. Runtime dependency declared by the source tree

This is the only non-standard-library package that `gca/` imports.

| Component | Version | Licence | Used for |
| --- | --- | --- | --- |
| [pypdf](https://github.com/py-pdf/pypdf) | `>=5.0,<7` (6.13.2 observed) | BSD-3-Clause | Text extraction on the PDF Reader page (`gca/tabs/reading.py`). |

Everything else the application imports (`tkinter`, `sqlite3`, `urllib`, `csv`, `json`, `zipfile`,
`ctypes`, `subprocess`, `unicodedata`, …) is part of the Python standard library and is covered by
the Python licence in section 2.

---

## 2. Runtime platform embedded in the frozen applications

PyInstaller copies the interpreter and its native support libraries into
`GermanCourseAI.exe` / `GermanCourseAI.app`. These are redistributed as-is, unmodified.

| Component | Version | Licence | Used for |
| --- | --- | --- | --- |
| [CPython](https://www.python.org/) (`python311.dll`, `python3.dll`, `base_library.zip`, stdlib `.pyd` modules) | 3.11 | PSF License Agreement (PSF-2.0) | The Python interpreter and standard library the application runs on. |
| [Tcl](https://www.tcl-lang.org/) / [Tk](https://www.tcl-lang.org/) (`tcl86t.dll`, `tk86t.dll`, `_tcl_data/`, `_tk_data/`) | 8.6 | Tcl/Tk licence (BSD-style, permissive) | The GUI toolkit behind `tkinter` — every window, tab and widget. |
| [SQLite](https://www.sqlite.org/) (`sqlite3.dll`, `_sqlite3.pyd`) | 3.45.1 | Public domain (SQLite blessing) | The local database that stores profiles, words, SRS state, exams and PDF notes. |
| [OpenSSL](https://www.openssl.org/) (`libcrypto-3.dll`, `libssl-3.dll`, `_ssl.pyd`) | 3.0.13 | Apache-2.0 | HTTPS for the optional alternative AI endpoint. |
| [libffi](https://sourceware.org/libffi/) (`libffi-8.dll`, `_ctypes.pyd`) | bundled with CPython 3.11 | MIT | Backs `ctypes`, used by the Windows Credential Manager key store (`gca/secrets.py`). |
| [Expat](https://libexpat.github.io/) (`pyexpat.pyd`, `_elementtree.pyd`) | bundled with CPython 3.11 | MIT | XML parsing in the standard library. |
| [bzip2 / libbzip2](https://sourceware.org/bzip2/) (`_bz2.pyd`) | 1.0.8 | bzip2 licence (BSD-style) | `bz2` support in the standard library. |
| [XZ Utils / liblzma](https://tukaani.org/xz/) (`_lzma.pyd`) | bundled with CPython 3.11 | 0BSD / public domain | `lzma` support in the standard library. |
| [zlib](https://zlib.net/) (linked into `python311.dll`) | bundled with CPython 3.11 | Zlib licence | `zipfile` / `zlib`, used by the `.gcapack` export and import. |
| Microsoft Universal C Runtime and VC++ redistributable (`ucrtbase.dll`, `VCRUNTIME140*.dll`, `msvcp140-*.dll`, `api-ms-win-*.dll`) | Windows build only | Microsoft Distributable Code (redistributable, proprietary) | C/C++ runtime required by the interpreter and the extension modules on Windows. |

The file names in the table above are those of the **Windows** build. The macOS `.app` ships the
same components under different names — `Contents/Frameworks/Python.framework/Versions/3.11/Python`
(CPython), `libtcl8.6.dylib` / `libtk8.6.dylib` (Tcl/Tk), `libcrypto.3.dylib` / `libssl.3.dylib`
(OpenSSL) and the `lib-dynload/*.cpython-311-darwin.so` extension modules such as `_sqlite3`,
`_bz2` and `_lzma` — under exactly the same licences. `libffi` is **not** bundled on macOS; the
system copy is used. The Microsoft Distributable Code row applies to the Windows build only.

The Microsoft Distributable Code is redistributed under the terms reproduced in the CPython
Windows `LICENSE.txt`: its copyright, trademark and patent notices must not be altered, Microsoft
trademarks must not be used in a way that suggests endorsement, and the code must not be shipped
for non-Microsoft platforms.

---

## 3. Additional Python packages present in the released Windows binary

The `1.2.1` Windows one-file build (`dist/GermanCourseAI.exe`) was produced on a machine with a
shared Python installation, and PyInstaller's dependency analysis pulled in a number of packages
that the application itself never imports — mostly through pypdf's optional integrations. They are
listed here because they are genuinely present in that binary and therefore genuinely redistributed.
All of them are permissive; none is copyleft.

| Component | Version | Licence | Why it is in the binary |
| --- | --- | --- | --- |
| [NumPy](https://numpy.org/) | 2.4.6 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | Collected as an optional dependency; not imported by `gca/`. |
| [OpenBLAS](https://www.openblas.net/) (`numpy.libs/libscipy_openblas64_*.dll`) | shipped inside the NumPy wheel | BSD-3-Clause; the same DLL also statically links [LAPACK](https://github.com/OpenMathLib/OpenBLAS/) (BSD-3-Clause-Open-MPI) and the **GCC Fortran runtime** (GPL-3.0-or-later **WITH** GCC-exception-3.1) | NumPy's linear-algebra backend. |
| [Pillow](https://python-pillow.github.io/) (`PIL`) | 12.2.0 | MIT-CMU (HPND) | pypdf's optional image support. |
| [cryptography](https://cryptography.io/) | 50.0.0 | Apache-2.0 OR BSD-3-Clause | pypdf's optional support for encrypted PDFs. |
| [cffi](https://github.com/python-cffi/cffi) (`_cffi_backend.cp311-win_amd64.pyd`) | 2.0.0 | MIT | Collected behind `cryptography`; not imported by `gca/`. |
| [typing_extensions](https://github.com/python/typing_extensions) | 4.15.0 | PSF-2.0 | Collected as an optional dependency of the packages above. |
| [lxml](https://lxml.de/) and [lxml_html_clean](https://github.com/fedora-python/lxml_html_clean) | 6.1.1 / 0.4.5 | BSD-3-Clause (bundling libxml2 and libxslt, both MIT) | Collected as an optional dependency; not imported by `gca/`. |
| [fontTools](https://github.com/fonttools/fonttools) | 4.63.0 | MIT | pypdf's optional font handling. |
| [PyYAML](https://pyyaml.org/) (bundling [libyaml](https://pyyaml.org/wiki/LibYAML), MIT) | 6.0.3 | MIT | Collected as an optional dependency; not imported by `gca/`. |
| [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) (`bs4`) | 4.15.0 | MIT | Collected as an optional dependency; not imported by `gca/`. |
| [soupsieve](https://github.com/facelessuser/soupsieve) | 2.8.4 | MIT | Beautiful Soup's CSS selector engine. |
| [charset-normalizer](https://github.com/jawah/charset_normalizer) | 3.4.7 | MIT | Collected as an optional dependency; not imported by `gca/`. |
| [defusedxml](https://github.com/tiran/defusedxml) | 0.7.1 | PSF-2.0 | Collected as an optional dependency; not imported by `gca/`. |
| [pywin32](https://github.com/mhammond/pywin32) (`pywintypes311.dll`, `win32pdh.pyd`) | 312 | PSF-style licence (as declared by the package) | Pulled in by PyInstaller's Windows runtime hook. |

Pillow's C extensions statically link further permissive libraries — libjpeg-turbo (BSD-3-Clause /
IJG), libtiff (libtiff licence), Little CMS (MIT), libwebp (BSD-3-Clause), OpenJPEG (BSD-2-Clause),
libavif with AOM/dav1d (BSD-2-Clause), libpng (PNG Reference Library License), zlib (Zlib) and
xz (0BSD). FreeType, HarfBuzz and Brotli are **not** part of this build: they are reachable only
through Pillow's `_imagingft` module, and that module is absent from the binary.

NumPy's OpenBLAS DLL statically links the **GCC Fortran runtime** (libgfortran). NumPy's own wheel
licence file declares it as **GPL-3.0-or-later WITH GCC-exception-3.1**. The GCC Runtime Library
Exception explicitly permits propagating a work that merely contains this runtime under any
licence, so it creates no copyleft obligation for German Course AI; it is listed here because the
code is genuinely redistributed inside the Windows executable. The macOS build does not contain
NumPy at all, so no libgfortran code is in the `.app`.

> **Maintenance note.** These packages are collected accidentally and account for most of the
> 44 MB of the Windows executable. Adding an `excludes=[...]` list to `GermanCourseAI.spec` (or
> building in a clean virtual environment that only holds `requirements-dev.txt`) would drop them.
> If that is done, this section should be reduced to whatever the new build actually contains.
>
> The released macOS artifact is produced by CI (`.github/workflows/build-macos.yml`) on a clean
> `macos-latest` runner from `requirements.txt`, and a scan of the shipped
> `GermanCourseAI-macOS.zip` confirms it contains **none** of the packages in this section — only
> pypdf. `build_macos.sh` creates a dedicated virtual environment under `build/macos/venv` and
> installs into that, so a local run cannot inherit whatever else happens to be present in the
> developer's interpreter.

---

## 4. Build-time tools

| Component | Version | Licence | Used for |
| --- | --- | --- | --- |
| [PyInstaller](https://pyinstaller.org/) | `>=6.0,<7` (6.21.0 observed) | GPL-2.0-or-later **WITH** the PyInstaller bootloader exception | Freezes the application into `GermanCourseAI.exe` and `GermanCourseAI.app`. |
| [pyinstaller-hooks-contrib](https://github.com/pyinstaller/pyinstaller-hooks-contrib) | 2026.6 | Apache-2.0 and GPL-2.0-or-later with the same exception | Package-specific PyInstaller hooks. |
| [UPX](https://upx.github.io/) | optional | GPL-2.0-or-later with the UPX special exception | `GermanCourseAI.spec` sets `upx=True`; when a UPX binary is on `PATH` the executable is compressed and a UPX decompression stub is embedded. UPX was **not** installed when the released `1.2.1` binary was built, so no UPX code is present in it. |
| [pytest](https://pytest.org/) | `>=8.0,<10` | MIT | Runs the test suite. Never shipped. |

PyInstaller's licence carries an explicit exception: the bootloader that ends up inside the frozen
executable may be distributed as part of an application under **any** licence, including MIT and
including proprietary ones. Using PyInstaller therefore does **not** make German Course AI a GPL
work and does **not** oblige anyone to publish sources under the GPL. The same holds for the UPX
stub under the UPX License Agreement's special permission. The PyInstaller and UPX programs
themselves remain GPL-2.0-or-later.

PyInstaller is a build tool, but two kinds of PyInstaller file do end up **inside** the frozen
executable and are therefore redistributed with it:

* the bootloader and the loader modules from `PyInstaller/loader` (`pyiboot01_bootstrap`,
  `pyimod01_archive`, `pyimod02_importers`, `pyimod03_ctypes`, `pyimod04_pywin32`) — covered by
  the bootloader exception quoted above;
* five run-time hooks — `pyi_rth_inspect`, `pyi_rth__tkinter`, `pyi_rth_pkgutil`,
  `pyi_rth_multiprocessing` from `PyInstaller/hooks/rthooks`, and
  `pyi_rth_cryptography_openssl` from `_pyinstaller_hooks_contrib/rthooks` — which PyInstaller
  licenses under **Apache-2.0**, not under the GPL: see the "Run-time Hooks" clause in
  `COPYING.txt` in the PyInstaller distribution and the `SPDX-License-Identifier: Apache-2.0`
  header on each file.

---

## 5. Obligations, grouped by licence family

* **MIT, BSD-2-Clause, BSD-3-Clause, MIT-CMU/HPND, Zlib, libtiff, PNG, bzip2, Tcl/Tk, PSF-2.0,
  PSF-style** — permissive. The obligation is attribution: keep the copyright notice and the
  licence text with any binary distribution. This file and `LICENSE` are shipped inside every
  release archive next to the executable (see [section 7](#7-what-ships-with-the-binaries)) and are
  published in the source repository, which satisfies that. BSD-3-Clause additionally forbids using
  the original authors' names to endorse this project; German Course AI makes no such claim.
* **Apache-2.0** (OpenSSL, `cryptography` where the Apache option is taken, and the PyInstaller
  run-time hooks embedded in the frozen executable) — permissive with a patent grant. If a
  component's distribution carries a `NOTICE` file, that notice must travel with redistributions;
  neither OpenSSL 3.0, nor `cryptography`, nor PyInstaller ships a `NOTICE` file requiring extra
  text beyond the attribution above.
* **0BSD, CC0-1.0, public domain** (parts of NumPy, xz, SQLite) — no obligation at all.
* **GPL-2.0-or-later with a linking/bootloader exception** (PyInstaller, optionally UPX) — the
  tools themselves are never shipped; what they embed in the executable is the bootloader and the
  `PyInstaller/loader` modules, and the exception covers exactly those, see section 4. It is what
  allows the frozen binary to stay MIT.
* **GPL-3.0-or-later with the GCC Runtime Library Exception 3.1** (libgfortran, statically linked
  inside NumPy's OpenBLAS DLL in the Windows binary) — the exception grants permission to
  propagate a work that merely contains this runtime under any licence, so there is **no**
  copyleft obligation and no source-disclosure requirement for German Course AI. This is the only
  GPL-licensed library code in any released binary. Removing NumPy from the Windows build (see the
  maintenance note in section 3) would remove it entirely.
* **Microsoft Distributable Code** — redistributable under the restrictions quoted at the end of
  section 2.
* **No MPL-2.0 component is used.** Had one been present, its files would have had to stay
  available in their original form under MPL-2.0 even inside an MIT-licensed distribution; the
  note is kept here only so the absence is explicit.
* **No LGPL or AGPL library, and no GPL library without an exception, is linked into or bundled
  with the binaries.**

---

## 6. External learning material (linked, never bundled)

The **Resource Center** page (`gca/content.py`, `RESOURCES`) shows four openly licensed catalogues
with their licence and attribution visible in the UI, and opens them in the user's browser on an
explicit click. German Course AI **does not download, cache, redistribute or bundle any of this
material** — none of it is in this repository or in the released binaries. Anything a user chooses
to fetch keeps its own licence and its own attribution requirements:

| Source | Licence as published |
| --- | --- |
| [German — Wikibooks](https://en.wikibooks.org/wiki/German) | CC BY-SA 4.0 — share-alike: derivative texts must stay under CC BY-SA and credit the Wikibooks contributors. |
| [Tatoeba sentence downloads](https://tatoeba.org/en/downloads) | CC BY 2.0 FR, with selected sentences under CC0 — sentence-level attribution must be preserved. |
| [LibriVox German audiobooks](https://librivox.org/) | Public domain in the USA; status varies by country. |
| [Project Gutenberg German shelf](https://www.gutenberg.org/browse/languages/de) | Project Gutenberg public-domain terms; status varies by country and the Project Gutenberg trademark terms apply to redistribution. |

The learning content that *is* shipped — the A1 seed vocabulary (`gca/seed_words.py`), the built-in
DE/EN/TR dictionary (`gca/dict_data.py`), the orthography, pronunciation and grammar labs
(`gca/content.py`) and the offline grammar notes (`grammar/`) — was written for this project and is
covered by the project's own MIT licence. Files a learner places in `Resources/` are their own and
are never redistributed; only the placeholder `Resources/BURAYA_DERS_KOYUN.txt` is in the repository.

---

## 7. What ships with the binaries

The attribution obligation of every permissive licence above is discharged by shipping the notices
with the binaries, not only by publishing them in the repository. Both build pipelines therefore
place `LICENSE` and `THIRD_PARTY_NOTICES.md` into the distributed artifact:

| Artifact | Where the notices are |
| --- | --- |
| `GermanCourseAI-Windows.zip` | `LICENSE` and `THIRD_PARTY_NOTICES.md` sit next to `GermanCourseAI.exe` in the archive root; `build.bat` builds the exe and then assembles the zip from those three files. |
| `GermanCourseAI.exe` | The same two files are also embedded as PyInstaller data (`GermanCourseAI.spec`), so they are present even if the exe is copied out of the archive. |
| `GermanCourseAI.app` / `GermanCourseAI-macOS.zip` | `build_macos.sh` passes both files to PyInstaller with `--add-data`, so they land inside the bundle. |

Anyone redistributing a modified build must keep doing this; dropping the two files from
`datas` / `--add-data` / the zip would break the attribution requirement of every MIT, BSD and
HPND component listed above.

> **Note on already-published archives.** The `1.2.1` archives were assembled before this rule was
> added to the build scripts, so the copies already on the release page contain the executable
> alone. Both files must be attached to that release, or linked from its notes, until the next
> build regenerates the archives.

---

## 8. How to re-verify

```powershell
# licence of each installed dependency, straight from its metadata
python -c "import importlib.metadata as m; d=m.metadata('pypdf'); print(d['Version'], d.get('License-Expression') or d.get('License'))"

# what a frozen build really contains
python -m PyInstaller --noconfirm --clean GermanCourseAI.spec

# the libgfortran statically linked into NumPy's OpenBLAS DLL, and its licence
python -c "import numpy, pathlib; p=pathlib.Path(numpy.__file__).parents[1]/'numpy.libs'; print([f.name for f in p.glob('libscipy_openblas*.dll')])"
python -c "import importlib.metadata as m; print([f for f in m.files('numpy') if f.name=='LICENSE.txt'])"  # 'Name: GCC runtime library'

# the notices really are inside the release archive
python -c "import zipfile; print(zipfile.ZipFile('dist/GermanCourseAI-Windows.zip').namelist())"
```

Please open an issue if a component is missing from this list or a licence is stated incorrectly.
