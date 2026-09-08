#!/usr/bin/env python3
"""Kullanim kilavuzlarini tek uretim hattiyla yeniden uretir / Rebuild the user guides.

Markdown -> HTML (docs/*.html, gitignored ara cikti) -> PDF (docs/*.pdf, surumle
birlikte dagitilan artefakt).

Kullanim / Usage:
    python -m pip install -r requirements-dev.txt
    python docs/build_guides.py

PDF, headless Chrome'un "print to PDF" motoruyla uretilir; Chrome yolu
CHROME_BIN ortam degiskeniyle verilebilir.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import markdown
except ModuleNotFoundError:  # pragma: no cover - kurulum uyarisi
    sys.exit("markdown paketi gerekli: python -m pip install -r requirements-dev.txt")

DOCS = Path(__file__).resolve().parent

# HTML govdesi bu ayarlarla uretilir; degistirilirse tum PDF yeniden dizilir.
MD_EXTENSIONS = ["extra", "toc"]
MD_OUTPUT_FORMAT = "xhtml"

STYLE = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Calibri", system-ui, sans-serif; font-size: 10.5pt; line-height: 1.55; color: #14171d; margin: 0; }
h1 { font-size: 24pt; margin: 0 0 4pt; color: #B8860B; border-bottom: 3px solid #B8860B; padding-bottom: 8pt; }
h2 { font-size: 15pt; margin: 22pt 0 6pt; color: #B8860B; border-bottom: 1px solid #d7dbe2; padding-bottom: 3pt; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 4pt; color: #1d2430; page-break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt; color: #38404f; page-break-after: avoid; }
p, li { orphans: 2; widows: 2; }
ul, ol { padding-left: 20pt; margin: 5pt 0; }
li { margin: 2pt 0; }
code { font-family: "Cascadia Mono", Consolas, monospace; font-size: 9pt; background: #eef1f6; padding: 1pt 3pt; border-radius: 3px; }
pre { background: #f4f6fa; border: 1px solid #dde2ea; border-left: 3px solid #B8860B; border-radius: 4px; padding: 8pt 10pt;
      overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 8.8pt; line-height: 1.4; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.4pt; page-break-inside: avoid; }
th { background: #B8860B; color: #fff; text-align: left; padding: 5pt 7pt; font-weight: 600; }
td { border-bottom: 1px solid #dfe4ec; padding: 5pt 7pt; vertical-align: top; }
tr:nth-child(even) td { background: #f7f9fc; }
blockquote { margin: 8pt 0; padding: 6pt 12pt; background: #f4f6fa; border-left: 3px solid #B8860B; color: #38404f; }
a { color: #B8860B; text-decoration: none; }
hr { border: none; border-top: 1px solid #dfe4ec; margin: 14pt 0; }
.subtitle { color: #5b6474; font-size: 10pt; margin: 0 0 14pt; }
"""

GUIDES = [
    ("KULLANIM_KILAVUZU", "tr", "German Course AI - Kullanım Kılavuzu"),
    ("USER_GUIDE", "en", "German Course AI - User Guide"),
]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def find_chrome() -> str:
    override = os.environ.get("CHROME_BIN")
    if override:
        return override
    for cand in CHROME_CANDIDATES:
        if os.path.isfile(cand):
            return cand
        found = shutil.which(cand)
        if found:
            return found
    sys.exit("Chrome bulunamadi. CHROME_BIN ortam degiskeniyle yolunu verin.")


def render_html(stem: str, lang: str, title: str) -> Path:
    md_path = DOCS / f"{stem}.md"
    body = markdown.markdown(
        md_path.read_text(encoding="utf-8"),
        extensions=MD_EXTENSIONS,
        output_format=MD_OUTPUT_FORMAT,
    )
    html = (
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        f"<title>{title}</title>\n<style>{STYLE}</style></head><body>{body}</body></html>"
    )
    out = DOCS / f"{stem}.html"
    out.write_text(html, encoding="utf-8")
    return out


def render_pdf(chrome: str, html_path: Path, pdf_path: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="gca-guide-chrome-") as profile:
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={profile}",
                "--no-pdf-header-footer",
                "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=20000",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            check=True,
        )


def main() -> int:
    chrome = find_chrome()
    for stem, lang, title in GUIDES:
        html_path = render_html(stem, lang, title)
        pdf_path = DOCS / f"{stem}.pdf"
        render_pdf(chrome, html_path, pdf_path)
        print(f"{html_path.name} -> {pdf_path.name} ({pdf_path.stat().st_size} bayt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
