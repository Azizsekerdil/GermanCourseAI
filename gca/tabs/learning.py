from __future__ import annotations

import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .. import config as C
from ..quiz_engine import Question, accuracy, build_session, check_answer
from ..srs import review
from ..transfer import export_csv, import_csv
from ..ui import BaseTab, clear, metric


class StudyTab(BaseTab):
    key, subtitle_key = "tab.study", "study.subtitle"
    def build(self):
        self.heading(); self.session = []; self.index = 0; self.revealed = False; self.correct = self.wrong = 0
        stats = ttk.Frame(self); stats.pack(fill="x", pady=(0, 12))
        d = self.repos.progress.dashboard(self.pid)
        for i, (title, value) in enumerate(((self.t("study.due"), d["due"]), (self.t("study.new"), d["new"]),
                                            (self.t("study.wrong"), len(self.repos.progress.wrong_words(self.pid))),
                                            (self.t("study.favorites"), len(self.repos.progress.starred(self.pid))))):
            c, _ = metric(stats, title, str(value)); c.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 5, 0))
            stats.columnconfigure(i, weight=1)
        controls = ttk.Frame(self); controls.pack(fill="x", pady=(0, 10))
        self.queue = tk.StringVar(value="new"); self.mode = tk.StringVar(value=self.t("study.cards")); self.limit = tk.IntVar(value=10)
        queue_box = ttk.Combobox(controls, textvariable=self.queue, state="readonly", width=14,
                                 values=("new", "due", "wrong", "favorites")); queue_box.pack(side="left", padx=(0, 8))
        ttk.Combobox(controls, textvariable=self.mode, state="readonly", width=20,
                     values=[self.t(k) for k in ("study.cards", "study.mcq", "study.typing", "study.listening", "study.matching")]).pack(side="left", padx=8)
        ttk.Spinbox(controls, from_=5, to=50, textvariable=self.limit, width=5).pack(side="left", padx=8)
        ttk.Button(controls, text=self.t("g.start"), style="Accent.TButton", command=lambda: self.start(self.queue.get())).pack(side="left", padx=8)
        self.stage = self.card(); self.stage.pack(fill="both", expand=True)
        self.status = ttk.Label(self.stage, text=self.t("study.no_words"), style="CardMuted.TLabel")
        self.status.pack(pady=30)

    def start(self, queue="new"):
        getters = {"new": self.repos.progress.new_words, "due": self.repos.progress.due_words,
                   "wrong": self.repos.progress.wrong_words, "favorites": self.repos.progress.starred}
        self.session = getters.get(queue, getters["new"])(self.pid, self.limit.get()) if queue != "favorites" else getters[queue](self.pid)[:self.limit.get()]
        self.index = self.correct = self.wrong = 0; self.render()

    def render(self):
        clear(self.stage)
        if not self.session:
            ttk.Label(self.stage, text=self.t("study.complete") if self.index else self.t("study.no_words"), style="Card.TLabel", font=("Segoe UI", 18, "bold")).pack(pady=70)
            return
        word = self.session[0]; self.revealed = False
        ttk.Label(self.stage, text=f"{self.index + 1} / {self.index + len(self.session)}", style="CardMuted.TLabel").pack(anchor="e")
        article = f"{word['article']} " if word.get("article") else ""
        ttk.Label(self.stage, text=f"{article}{word['target']}", style="Card.TLabel", font=("Segoe UI", 32, "bold")).pack(pady=(45, 8))
        ttk.Label(self.stage, text=f"{word.get('plural','')}  ·  {word.get('pos','')}", style="CardMuted.TLabel").pack()
        self.answer = ttk.Label(self.stage, text="", style="Card.TLabel", font=("Segoe UI", 16))
        self.answer.pack(pady=20)
        self.actions = ttk.Frame(self.stage, style="Card.TFrame"); self.actions.pack(pady=8)
        ttk.Button(self.actions, text=self.t("study.show"), style="Accent.TButton", command=self.reveal).pack()
        if self.mode.get() == self.t("study.listening"):
            self.app.speak(word["target"])

    def reveal(self):
        if not self.session: return
        word = self.session[0]; self.revealed = True
        self.answer.configure(text=f"{word['tr']}  ·  {word['en']}\n{word['example_target']}")
        clear(self.actions)
        for key, quality in (("study.again", 1), ("study.hard", 3), ("study.good", 4), ("study.easy", 5)):
            ttk.Button(self.actions, text=self.t(key), command=lambda q=quality: self.grade(q)).pack(side="left", padx=5)

    def grade(self, quality):
        if not self.session: return
        word = self.session.pop(0); state = review(self.repos.progress.state(self.pid, word["id"]), quality)
        ok = quality >= 3; self.correct += int(ok); self.wrong += int(not ok)
        self.repos.progress.save(self.pid, word["id"], state, int(ok), int(not ok)); self.index += 1
        if not self.session: self.repos.study.log(self.pid, "srs", self.correct, self.wrong)
        self.render()


class WordsTab(BaseTab):
    key, subtitle_key = "tab.words", "words.subtitle"
    def build(self):
        self.heading(); bar = ttk.Frame(self); bar.pack(fill="x", pady=(0, 9))
        self.query = tk.StringVar(); entry = ttk.Entry(bar, textvariable=self.query); entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda _e: self.refresh())
        ttk.Button(bar, text=self.t("g.search"), command=self.refresh).pack(side="left", padx=5)
        ttk.Button(bar, text=f"↓ {self.t('g.import')}", command=self.import_file).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↑ {self.t('g.export')}", command=self.export_file).pack(side="right", padx=3)
        cols = ("target", "tr", "en", "article", "plural", "deck")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for col, title, width in zip(cols, (self.t("words.target"), self.t("words.tr"), self.t("words.en"), self.t("words.article"), self.t("words.plural"), self.t("words.deck")), (180, 170, 170, 65, 130, 120)):
            self.tree.heading(col, text=title); self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True); self.tree.bind("<<TreeviewSelect>>", self.selected)
        self.detail = ttk.Label(self, text="", style="Muted.TLabel", wraplength=980); self.detail.pack(anchor="w", pady=8)
        ttk.Button(self, text="★ " + self.t("words.star"), command=self.toggle_star).pack(anchor="e")
        self.rows = {}; self.refresh()
    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.rows = {}
        for w in self.repos.words.search(self.query.get()):
            iid = str(w["id"]); self.rows[iid] = w
            self.tree.insert("", "end", iid=iid, values=(w["target"], w["tr"], w["en"], w["article"], w["plural"], w["deck"]))
    def selected(self, _event=None):
        sel = self.tree.selection()
        if not sel: return
        w = self.rows[sel[0]]; self.detail.configure(text=f"{w['example_target']}  —  {w['example_tr']}  —  {w['example_en']}")
    def toggle_star(self):
        sel = self.tree.selection()
        if sel: self.repos.progress.toggle_star(self.pid, int(sel[0]))
    def export_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[(self.t("words.csv"), "*.csv")])
        if path: export_csv(self.repos.words.all(), path)
    def import_file(self):
        path = filedialog.askopenfilename(filetypes=[(self.t("words.csv"), "*.csv")])
        if path: import_csv(self.repos.words, path); self.refresh()


class ExamTab(BaseTab):
    key, subtitle_key = "tab.exam", "exam.subtitle"
    def build(self):
        self.heading(); bar = ttk.Frame(self); bar.pack(fill="x")
        self.count = tk.IntVar(value=10); ttk.Label(bar, text=self.t("exam.count")).pack(side="left")
        ttk.Spinbox(bar, from_=5, to=50, textvariable=self.count, width=5).pack(side="left", padx=8)
        ttk.Button(bar, text=self.t("g.start"), style="Accent.TButton", command=self.start).pack(side="left")
        self.stage = self.card(); self.stage.pack(fill="both", expand=True, pady=12)
        self.questions = []; self.results = []; self.idx = 0; self.exam_id = None
    def start(self):
        words = self.repos.words.all(); self.questions = build_session(words, self.count.get(), random.Random())
        self.results = []; self.idx = 0; self.exam_id = self.repos.exams.start(self.pid, "mcq", self.app.settings["cefr"]); self.render()
    def render(self):
        clear(self.stage)
        if self.idx >= len(self.questions):
            summary = self.repos.exams.finish(self.exam_id); self.repos.study.log(self.pid, "exam", summary["correct"], summary["total"]-summary["correct"])
            ttk.Label(self.stage, text=f"{self.t('exam.finish')}\n{self.t('exam.score')}: {summary['score']}%", style="Card.TLabel", font=("Segoe UI", 24, "bold")).pack(pady=80); return
        q = self.questions[self.idx]; ttk.Label(self.stage, text=f"{self.idx+1} / {len(self.questions)}", style="CardMuted.TLabel").pack(anchor="e")
        ttk.Label(self.stage, text=q.prompt, style="Card.TLabel", font=("Segoe UI", 24, "bold")).pack(pady=(45, 22))
        self.choice = tk.StringVar()
        for option in q.options: ttk.Radiobutton(self.stage, text=option, value=option, variable=self.choice).pack(anchor="center", pady=3)
        ttk.Button(self.stage, text=self.t("g.check"), style="Accent.TButton", command=self.submit).pack(pady=20)
    def submit(self):
        q = self.questions[self.idx]; given = self.choice.get(); ok = check_answer(q, given); self.results.append(ok)
        self.repos.exams.answer(self.exam_id, q.word_id, q.kind, q.prompt, given, q.answer, ok); self.idx += 1; self.render()
