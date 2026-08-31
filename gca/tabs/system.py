from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .. import config as C
from ..transfer import export_pack, import_pack
from ..ui import BaseTab, metric


class ProgressTab(BaseTab):
    key, subtitle_key = "tab.progress", "progress.subtitle"
    def build(self):
        self.heading(); self.stats = ttk.Frame(self); self.stats.pack(fill="x", pady=(0, 12))
        dashboard = self.repos.progress.dashboard(self.pid); streak = self.repos.study.streak(self.pid)
        values = (("progress.goal", self.app.settings["daily_goal"]), ("progress.streak", streak),
                  ("progress.seen", dashboard["seen"]), ("progress.learned", dashboard["learned"]))
        for i, (key, value) in enumerate(values):
            card, _ = metric(self.stats, self.t(key), str(value)); card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 5, 0)); self.stats.columnconfigure(i, weight=1)
        body = self.card(); body.pack(fill="both", expand=True)
        ttk.Label(body, text=self.t("progress.week"), style="Card.TLabel", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        self.chart = tk.Canvas(body, height=230, bg=self.palette["card"], highlightthickness=0); self.chart.pack(fill="x", pady=8)
        self.draw_chart()
        ttk.Label(body, text=self.t("progress.report"), style="CardMuted.TLabel").pack(anchor="w")
        days = self.repos.study.daily(self.pid, 7); correct = sum(int(d["correct"]) for d in days); wrong = sum(int(d["wrong"]) for d in days)
        ttk.Label(body, text=f"{self.t('exam.correct')}: {correct}   ·   {self.t('exam.wrong')}: {wrong}   ·   {self.t('exam.score')}: {round(100*correct/max(1,correct+wrong),1)}%",
                  style="Card.TLabel", font=("Segoe UI", 12)).pack(anchor="w", pady=6)
    def draw_chart(self):
        self.chart.delete("all"); days = self.repos.study.daily(self.pid, 7); width = max(700, self.chart.winfo_width() or 700); base = 195; maxv = max([int(d["correct"])+int(d["wrong"]) for d in days] + [1])
        gap = width / 7
        for i, day in enumerate(days):
            total = int(day["correct"]) + int(day["wrong"]); h = 145 * total / maxv; x0 = i*gap+24; x1 = (i+1)*gap-24
            self.chart.create_rectangle(x0, base-h, x1, base, fill=self.palette["accent"], outline="")
            self.chart.create_text((x0+x1)/2, 215, text=day["day"][5:], fill=self.palette["muted"], font=("Segoe UI", 9))
            self.chart.create_text((x0+x1)/2, base-h-10, text=str(total), fill=self.palette["fg"], font=("Segoe UI", 9, "bold"))


class PacksTab(BaseTab):
    key, subtitle_key = "tab.packs", "packs.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="x")
        self.include = tk.BooleanVar(value=False); ttk.Checkbutton(main, text=self.t("packs.include"), variable=self.include).pack(anchor="w")
        row = ttk.Frame(main, style="Card.TFrame"); row.pack(fill="x", pady=15)
        ttk.Button(row, text="↑ " + self.t("g.export"), style="Accent.TButton", command=self.export).pack(side="left")
        ttk.Button(row, text="↓ " + self.t("g.import"), command=self.import_).pack(side="left", padx=8)
        self.status = ttk.Label(main, text="", style="CardMuted.TLabel"); self.status.pack(anchor="w")
    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=C.PACK_EXTENSION, filetypes=[(C.APP_NAME, "*" + C.PACK_EXTENSION)])
        if path: export_pack(self.repos, self.pid, path, self.include.get()); self.status.configure(text=self.t("packs.created") + ": " + path)
    def import_(self):
        path = filedialog.askopenfilename(filetypes=[(C.APP_NAME, "*" + C.PACK_EXTENSION)])
        if path:
            count = import_pack(self.repos, self.pid, path); self.status.configure(text=f"{self.t('packs.loaded')}: {count}")


class TokensTab(BaseTab):
    key, subtitle_key = "tab.tokens", "tokens.subtitle"
    def build(self):
        self.heading(); summary = self.repos.tokens.summary(); stats = ttk.Frame(self); stats.pack(fill="x", pady=(0, 10))
        for i, (title, value) in enumerate(((self.t("tokens.calls"), summary["calls"]), (self.t("tokens.total"), summary["tokens"]))):
            card, _ = metric(stats, title, str(value)); card.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 5, 0)); stats.columnconfigure(i, weight=1)
        cols = ("ts", "model", "task", "prompt_tokens", "completion_tokens", "total_tokens", "ms", "ok")
        tree = ttk.Treeview(self, columns=cols, show="headings")
        for col in cols: tree.heading(col, text=col.replace("_", " ").title()); tree.column(col, width=120 if col in ("ts", "model") else 90)
        for row in self.repos.tokens.rows(): tree.insert("", "end", values=tuple(row[c] for c in cols))
        tree.pack(fill="both", expand=True)
        ttk.Label(self, text="🔒 " + self.t("ai.privacy"), style="Muted.TLabel").pack(anchor="w", pady=8)


class GuideTab(BaseTab):
    key, subtitle_key = "tab.guide", "guide.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="both", expand=True)
        ttk.Label(main, text=self.t("guide.body"), style="Card.TLabel", justify="left", wraplength=900, font=("Segoe UI", 11)).pack(anchor="nw", pady=5)
        ttk.Separator(main).pack(fill="x", pady=20)
        ttk.Label(main, text=str(C.APP_HOME), style="CardMuted.TLabel").pack(anchor="w")


class SettingsTab(BaseTab):
    key, subtitle_key = "tab.settings", "settings.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="both", expand=True)
        grid = ttk.Frame(main, style="Card.TFrame"); grid.pack(fill="x"); grid.columnconfigure(1, weight=1)
        self.theme = tk.StringVar(value=self.app.settings["theme"]); self.goal = tk.IntVar(value=self.app.settings["daily_goal"])
        self.tts = tk.BooleanVar(value=self.app.settings["tts_enabled"]); self.ai = tk.BooleanVar(value=self.app.settings["ai_enabled"])
        self.base = tk.StringVar(value=self.app.settings["ai_base"]); self.model = tk.StringVar(value=self.app.settings["ai_model"])
        self.nim = tk.BooleanVar(value=self.app.settings["nim_enabled"])
        rows = [
            ("settings.theme", ttk.Combobox(grid, textvariable=self.theme, state="readonly", values=("dark", "light"))),
            ("settings.goal", ttk.Spinbox(grid, from_=5, to=200, textvariable=self.goal)),
            ("settings.tts", ttk.Checkbutton(grid, variable=self.tts)),
            ("settings.ai", ttk.Checkbutton(grid, variable=self.ai)),
            ("settings.base", ttk.Entry(grid, textvariable=self.base)),
            ("settings.model", ttk.Combobox(grid, textvariable=self.model, values=sum(C.MODEL_PROFILES.values(), []))),
            ("settings.nim", ttk.Checkbutton(grid, variable=self.nim)),
        ]
        for i, (key, widget) in enumerate(rows):
            ttk.Label(grid, text=self.t(key), style="Card.TLabel").grid(row=i, column=0, sticky="w", pady=7, padx=(0, 18)); widget.grid(row=i, column=1, sticky="ew", pady=7)
        ttk.Label(main, text="🔒 " + self.t("settings.secrets"), style="CardMuted.TLabel").pack(anchor="w", pady=12)
        bar = ttk.Frame(main, style="Card.TFrame"); bar.pack(fill="x")
        ttk.Button(bar, text=self.t("g.save"), style="Accent.TButton", command=self.save).pack(side="left")
        self.saved = ttk.Label(bar, text="", style="CardMuted.TLabel"); self.saved.pack(side="left", padx=10)
    def save(self):
        old_theme = self.app.settings["theme"]
        self.app.settings.update({"theme": self.theme.get(), "daily_goal": self.goal.get(), "tts_enabled": self.tts.get(),
                                  "ai_enabled": self.ai.get(), "ai_base": self.base.get().strip(), "ai_model": self.model.get().strip(),
                                  "nim_enabled": self.nim.get()})
        C.save_settings(self.app.settings); self.saved.configure(text=self.t("settings.saved"))
        if old_theme != self.theme.get(): self.app.apply_theme_and_rebuild()
