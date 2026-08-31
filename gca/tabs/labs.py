from __future__ import annotations

import random
import tkinter as tk
from tkinter import messagebox, ttk

from .. import content
from ..ui import BaseTab, clear


class OrthographyTab(BaseTab):
    key, subtitle_key = "tab.orthography", "lab.subtitle"
    def build(self):
        self.heading(); pane = ttk.Panedwindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = self.card(pane); right = self.card(pane); pane.add(left, weight=3); pane.add(right, weight=2)
        cols = ("symbol", "name", "example"); self.tree = ttk.Treeview(left, columns=cols, show="headings")
        for col, title, width in (("symbol", "", 90), ("name", self.t("lab.rules"), 190), ("example", self.t("words.example"), 230)):
            self.tree.heading(col, text=title); self.tree.column(col, width=width)
        for symbol, name, rule, example in content.ORTHOGRAPHY:
            self.tree.insert("", "end", values=(symbol, name, example), tags=(rule,))
        self.tree.pack(fill="both", expand=True); self.tree.bind("<<TreeviewSelect>>", self.show_rule)
        self.rule = ttk.Label(right, text=content.ORTHOGRAPHY[0][2], style="Card.TLabel", wraplength=330, justify="left")
        self.rule.pack(anchor="w", pady=(0, 24))
        ttk.Label(right, text=self.t("lab.dictation"), style="CardMuted.TLabel").pack(anchor="w")
        self.dictation_word = tk.StringVar(value="Straße"); self.dictation_answer = tk.StringVar()
        ttk.Button(right, text="▶ " + self.t("pron.speak"), command=lambda: self.app.speak(self.dictation_word.get())).pack(anchor="w", pady=8)
        ttk.Entry(right, textvariable=self.dictation_answer).pack(fill="x", pady=5)
        self.feedback = ttk.Label(right, text="", style="CardMuted.TLabel"); self.feedback.pack(anchor="w", pady=5)
        ttk.Button(right, text=self.t("g.check"), style="Accent.TButton", command=self.check).pack(anchor="w", pady=8)
    def show_rule(self, _event=None):
        sel = self.tree.selection()
        if sel: self.rule.configure(text=self.tree.item(sel[0], "tags")[0])
    def check(self):
        ok = self.app.answer_equal(self.dictation_answer.get(), self.dictation_word.get())
        self.feedback.configure(text="✓" if ok else f"→ {self.dictation_word.get()}")


class PronunciationTab(BaseTab):
    key, subtitle_key = "tab.pronunciation", "pron.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="both", expand=True)
        self.word = tk.StringVar(value="Mädchen")
        row = ttk.Frame(main, style="Card.TFrame"); row.pack(fill="x")
        ttk.Entry(row, textvariable=self.word, font=("Segoe UI", 18)).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="▶ " + self.t("pron.speak"), style="Accent.TButton", command=lambda: self.app.speak(self.word.get())).pack(side="left", padx=8)
        ttk.Button(row, text="◉ " + self.t("pron.record"), command=self.compare).pack(side="left")
        ttk.Separator(main).pack(fill="x", pady=18)
        ttk.Label(main, text=self.t("pron.tip"), style="CardMuted.TLabel").pack(anchor="w")
        for name, ipa, examples in content.PRONUNCIATION:
            line = ttk.Frame(main, style="Card.TFrame"); line.pack(fill="x", pady=4)
            ttk.Label(line, text=name, style="Card.TLabel", width=20, font=("Segoe UI", 11, "bold")).pack(side="left")
            ttk.Label(line, text=ipa, style="Card.TLabel", width=15).pack(side="left")
            ttk.Label(line, text=examples, style="CardMuted.TLabel").pack(side="left")
        self.result = ttk.Label(main, text="", style="CardMuted.TLabel"); self.result.pack(anchor="w", pady=15)
    def compare(self):
        self.result.configure(text=self.t("g.unavailable"))


class GrammarTab(BaseTab):
    key, subtitle_key = "tab.grammar", "grammar.subtitle"
    def build(self):
        self.heading(); pane = ttk.Panedwindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = self.card(pane, 8); right = self.card(pane); pane.add(left, weight=2); pane.add(right, weight=5)
        self.list = tk.Listbox(left, bg=self.palette["card"], fg=self.palette["fg"], selectbackground=self.palette["accent2"],
                               relief="flat", highlightthickness=0, font=("Segoe UI", 10))
        self.list.pack(fill="both", expand=True); self.topics = content.GRAMMAR_TOPICS
        for topic in self.topics: self.list.insert("end", topic["title"][self.app.ui_lang])
        self.list.bind("<<ListboxSelect>>", self.select_topic)
        self.title = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 18, "bold")); self.title.pack(anchor="w")
        self.rule = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=660, justify="left"); self.rule.pack(anchor="w", pady=(7, 8))
        self.example = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 13)); self.example.pack(anchor="w", pady=(0, 20))
        ttk.Separator(right).pack(fill="x", pady=8)
        ttk.Label(right, text=self.t("grammar.exercise"), style="CardMuted.TLabel").pack(anchor="w")
        self.prompt = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 15, "bold")); self.prompt.pack(anchor="w", pady=10)
        self.choice = tk.StringVar(); self.options = ttk.Frame(right, style="Card.TFrame"); self.options.pack(anchor="w")
        self.feedback = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=650); self.feedback.pack(anchor="w", pady=8)
        buttons = ttk.Frame(right, style="Card.TFrame"); buttons.pack(anchor="w", pady=8)
        ttk.Button(buttons, text=self.t("g.check"), style="Accent.TButton", command=self.check).pack(side="left")
        ttk.Button(buttons, text=self.t("g.next"), command=self.next_exercise).pack(side="left", padx=8)
        self.current = None; self.list.selection_set(0); self.select_topic(); self.next_exercise()
    def select_topic(self, _event=None):
        sel = self.list.curselection(); topic = self.topics[sel[0] if sel else 0]
        self.title.configure(text=topic["title"][self.app.ui_lang]); self.rule.configure(text=topic["rule"][self.app.ui_lang]); self.example.configure(text=topic["example"])
    def next_exercise(self):
        self.current = random.choice(content.EXERCISES); self.prompt.configure(text=self.current["prompt"]); self.choice.set(""); self.feedback.configure(text="")
        clear(self.options)
        for option in self.current["options"]: ttk.Radiobutton(self.options, text=option, value=option, variable=self.choice).pack(anchor="w")
    def check(self):
        if not self.current: return
        ok = self.app.answer_equal(self.choice.get(), self.current["answer"])
        self.feedback.configure(text=("✓ " if ok else f"→ {self.current['answer']} — ") + self.current["explain"])
        self.repos.grammar.record(self.pid, self.current["topic"], int(ok), int(not ok))
