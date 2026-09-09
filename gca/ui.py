from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk

from . import config as C

FONT = "Segoe UI"


def apply_theme(root: tk.Misc, style: ttk.Style, theme_name: str):
    p = C.PALETTES.get(theme_name, C.PALETTES["dark"])
    root.configure(bg=p["bg"])
    style.theme_use("clam")
    style.configure(".", background=p["bg"], foreground=p["fg"], font=(FONT, 10),
                    fieldbackground=p["card"], bordercolor=p["border"], lightcolor=p["border"], darkcolor=p["border"])
    style.configure("TFrame", background=p["bg"])
    style.configure("Card.TFrame", background=p["card"], relief="flat")
    style.configure("TLabel", background=p["bg"], foreground=p["fg"])
    style.configure("Card.TLabel", background=p["card"], foreground=p["fg"])
    style.configure("Muted.TLabel", background=p["bg"], foreground=p["muted"])
    style.configure("CardMuted.TLabel", background=p["card"], foreground=p["muted"])
    style.configure("Title.TLabel", background=p["bg"], foreground=p["fg"], font=(FONT, 21, "bold"))
    style.configure("Metric.TLabel", background=p["card"], foreground=p["accent"], font=(FONT, 22, "bold"))
    style.configure("Accent.TButton", background=p["accent"], foreground="#111111", borderwidth=0, padding=(14, 8))
    style.map("Accent.TButton", background=[("active", p["accent2"])], foreground=[("active", "white")])
    style.configure("TButton", background=p["card"], foreground=p["fg"], padding=(10, 7), borderwidth=1)
    style.map("TButton", background=[("active", p["hover"])])
    style.configure("TEntry", padding=7)
    style.configure("TCombobox", padding=6)
    style.configure("Treeview", background=p["card"], fieldbackground=p["card"], foreground=p["fg"], rowheight=27)
    style.configure("Treeview.Heading", background=p["panel"], foreground=p["fg"], font=(FONT, 9, "bold"))
    style.map("Treeview", background=[("selected", p["accent2"])], foreground=[("selected", "white")])
    style.configure("TNotebook", background=p["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=p["panel"], foreground=p["muted"], padding=(12, 7))
    style.map("TNotebook.Tab", background=[("selected", p["card"])], foreground=[("selected", p["fg"])])
    # Aqua only: it ignores the colours set on tk buttons and readonly comboboxes.
    if sys.platform == "darwin":
        style.configure("Nav.TButton", background=p["deep"], foreground=p["fg"],
                        anchor="w", padding=(14, 5), borderwidth=0, font=(FONT, 9))
        style.map("Nav.TButton", background=[("active", p["hover"])], foreground=[("active", p["fg"])])
        style.configure("Selected.Nav.TButton", background=p["card"], foreground=p["accent"])
        style.map("Selected.Nav.TButton", background=[("active", p["card"])], foreground=[("active", p["accent"])])
        style.map("TCombobox", fieldbackground=[("readonly", p["card"])],
                  foreground=[("readonly", p["fg"])], selectbackground=[("readonly", p["card"])],
                  selectforeground=[("readonly", p["fg"])])
    return p


def style_text(widget: tk.Text, palette: dict, mono: bool = False):
    widget.configure(background=palette["card"], foreground=palette["fg"], insertbackground=palette["accent"],
                     selectbackground=palette["accent2"], relief="flat", padx=12, pady=10,
                     font=("Cascadia Mono" if mono else FONT, 10), wrap="word", highlightthickness=1,
                     highlightbackground=palette["border"], highlightcolor=palette["accent"])


class BaseTab(ttk.Frame):
    key = ""
    subtitle_key = ""

    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.repos = app.repos
        self.palette = app.palette
        self.pid = app.profile_id
        self.build()

    def t(self, key: str) -> str: return self.app.t(key)
    def build(self) -> None: raise NotImplementedError
    def heading(self):
        ttk.Label(self, text=self.t(self.key), style="Title.TLabel").pack(anchor="w")
        ttk.Label(self, text=self.t(self.subtitle_key), style="Muted.TLabel").pack(anchor="w", pady=(2, 14))

    def card(self, parent=None, padding=14):
        frame = ttk.Frame(parent or self, style="Card.TFrame", padding=padding)
        return frame

    def text(self, parent, height=8, mono=False):
        box = tk.Text(parent, height=height)
        style_text(box, self.palette, mono)
        return box


def metric(parent, title: str, value: str):
    frame = ttk.Frame(parent, style="Card.TFrame", padding=14)
    ttk.Label(frame, text=title, style="CardMuted.TLabel").pack(anchor="w")
    label = ttk.Label(frame, text=value, style="Metric.TLabel")
    label.pack(anchor="w", pady=(4, 0))
    return frame, label


def clear(frame: tk.Misc):
    for child in frame.winfo_children():
        child.destroy()
