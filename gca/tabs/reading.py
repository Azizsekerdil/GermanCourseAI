from __future__ import annotations

import os
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk

from .. import config as C
from .. import content
from ..ui import BaseTab, clear


class ResourcesTab(BaseTab):
    key, subtitle_key = "tab.resources", "resources.subtitle"
    def build(self):
        self.heading(); ttk.Label(self, text="ⓘ " + self.t("resources.notice"), style="Muted.TLabel").pack(anchor="w", pady=(0, 8))
        self.container = ttk.Frame(self); self.container.pack(fill="both", expand=True)
        for resource in content.RESOURCES:
            card = self.card(self.container, 12); card.pack(fill="x", pady=4)
            top = ttk.Frame(card, style="Card.TFrame"); top.pack(fill="x")
            ttk.Label(top, text=resource["title"], style="Card.TLabel", font=("Segoe UI", 11, "bold")).pack(side="left")
            ttk.Label(top, text=resource["level"], style="CardMuted.TLabel").pack(side="right")
            ttk.Label(card, text=f"{self.t('resources.license')}: {resource['license']}", style="CardMuted.TLabel", wraplength=900).pack(anchor="w", pady=(5, 0))
            ttk.Label(card, text=f"{self.t('resources.attribution')}: {resource['attribution']}", style="CardMuted.TLabel", wraplength=900).pack(anchor="w")
            ttk.Button(card, text=self.t("g.open") + " ↗", command=lambda url=resource["url"]: webbrowser.open(url)).pack(anchor="e", pady=(4, 0))


class PDFTab(BaseTab):
    key, subtitle_key = "tab.pdf", "pdf.subtitle"
    def build(self):
        self.heading(); bar = ttk.Frame(self); bar.pack(fill="x")
        self.path = tk.StringVar(value=self.app.settings.get("last_pdf", "")); self.page = tk.IntVar(value=1)
        ttk.Button(bar, text=self.t("pdf.choose"), style="Accent.TButton", command=self.choose).pack(side="left")
        ttk.Label(bar, textvariable=self.path, style="Muted.TLabel").pack(side="left", fill="x", expand=True, padx=8)
        ttk.Label(bar, text=self.t("pdf.page")).pack(side="left"); ttk.Spinbox(bar, from_=1, to=9999, textvariable=self.page, width=6, command=self.load_page).pack(side="left", padx=5)
        pane = ttk.Panedwindow(self, orient="horizontal"); pane.pack(fill="both", expand=True, pady=10)
        text_card = self.card(pane); note_card = self.card(pane); pane.add(text_card, weight=3); pane.add(note_card, weight=1)
        self.viewer = self.text(text_card, height=20); self.viewer.pack(fill="both", expand=True)
        self.viewer.insert("1.0", self.t("pdf.no_file")); self.viewer.configure(state="disabled")
        ttk.Label(note_card, text=self.t("pdf.note"), style="CardMuted.TLabel").pack(anchor="w")
        self.note = self.text(note_card, height=12); self.note.pack(fill="both", expand=True, pady=8)
        ttk.Button(note_card, text=self.t("g.save"), command=self.save_note).pack(anchor="e")
        self.reader = None
        if self.path.get() and Path(self.path.get()).exists(): self.open_pdf(self.path.get())
    def choose(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path: self.open_pdf(path)
    def open_pdf(self, path):
        def work():
            from pypdf import PdfReader
            return PdfReader(path)
        def done(reader):
            self.reader = reader; self.path.set(path); self.page.set(1); self.app.settings["last_pdf"] = path; C.save_settings(self.app.settings); self.load_page()
        self.app.run_async(work, done)
    def load_page(self):
        if not self.reader: return
        index = max(0, min(len(self.reader.pages)-1, self.page.get()-1)); text = self.reader.pages[index].extract_text() or ""
        self.viewer.configure(state="normal"); self.viewer.delete("1.0", "end"); self.viewer.insert("1.0", text); self.viewer.configure(state="disabled")
        self.note.delete("1.0", "end"); self.note.insert("1.0", self.repos.notes.get(self.pid, self.path.get(), index+1))
    def save_note(self):
        if self.path.get(): self.repos.notes.save(self.pid, self.path.get(), self.page.get(), self.note.get("1.0", "end-1c"))


class LibraryTab(BaseTab):
    key, subtitle_key = "tab.library", "library.subtitle"
    def build(self):
        self.heading(); C.RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
        bar = ttk.Frame(self); bar.pack(fill="x", pady=(0, 8))
        ttk.Button(bar, text=self.t("library.folder"), style="Accent.TButton", command=self.open_folder).pack(side="left")
        ttk.Button(bar, text=self.t("g.refresh"), command=self.refresh).pack(side="left", padx=8)
        self.list = ttk.Treeview(self, columns=("name", "kind", "size"), show="headings")
        self.list.heading("name", text=self.t("g.name")); self.list.heading("kind", text=self.t("words.pos")); self.list.heading("size", text="MB")
        self.list.column("name", width=580); self.list.column("kind", width=100); self.list.column("size", width=100)
        self.list.pack(fill="both", expand=True); self.list.bind("<Double-1>", self.open_selected); self.paths = {}; self.refresh()
    def refresh(self):
        for item in self.list.get_children(): self.list.delete(item)
        self.paths = {}
        for path in sorted(C.RESOURCES_DIR.rglob("*")):
            if path.is_file() and path.name != "BURAYA_DERS_KOYUN.txt":
                iid = str(len(self.paths)); self.paths[iid] = path
                self.list.insert("", "end", iid=iid, values=(path.name, path.suffix.lower().lstrip("."), f"{path.stat().st_size/1048576:.1f}"))
    def open_folder(self):
        if os.name == "nt": os.startfile(C.RESOURCES_DIR)
    def open_selected(self, _event=None):
        sel = self.list.selection()
        if sel and os.name == "nt": os.startfile(self.paths[sel[0]])
