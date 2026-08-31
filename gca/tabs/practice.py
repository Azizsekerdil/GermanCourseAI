from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk

from ..ai_client import AIError
from ..ui import BaseTab, style_text


def _call_ai(tab, prompt: str, task: str, output: tk.Text, image_path: str = ""):
    if not tab.app.settings.get("ai_enabled") or not tab.app.ai.available():
        output.configure(state="normal"); output.delete("1.0", "end"); output.insert("1.0", tab.t("ai.status_off")); output.configure(state="disabled"); return
    output.configure(state="normal"); output.delete("1.0", "end"); output.insert("1.0", "…"); output.configure(state="disabled")
    def work():
        return tab.app.ai.chat(prompt, task, tab.app.ui_lang, tab.app.settings.get("ai_model", ""), image_path=image_path)
    def done(text):
        output.configure(state="normal"); output.delete("1.0", "end"); output.insert("1.0", text); output.configure(state="disabled")
    def error(_exc):
        output.configure(state="normal"); output.delete("1.0", "end"); output.insert("1.0", tab.t("ai.status_off")); output.configure(state="disabled")
    tab.app.run_async(work, done, error)


class AITab(BaseTab):
    key, subtitle_key = "tab.ai", "ai.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="both", expand=True)
        bar = ttk.Frame(main, style="Card.TFrame"); bar.pack(fill="x")
        self.task = tk.StringVar(value=self.t("ai.explain")); self.task_map = {
            self.t("ai.explain"): "grammar", self.t("ai.translate"): "translate", self.t("ai.correct"): "correct", self.t("ai.vision"): "vision"}
        ttk.Label(bar, text=self.t("ai.task"), style="CardMuted.TLabel").pack(side="left")
        ttk.Combobox(bar, textvariable=self.task, state="readonly", values=list(self.task_map), width=19).pack(side="left", padx=8)
        ttk.Button(bar, text=self.t("ai.send"), style="Accent.TButton", command=self.send).pack(side="right")
        ttk.Button(bar, text=self.t("ai.vision"), command=self.choose_image).pack(side="right", padx=8)
        self.input = self.text(main, height=7); self.input.pack(fill="x", pady=10)
        self.output = self.text(main, height=14); self.output.pack(fill="both", expand=True); self.output.configure(state="disabled")
        ttk.Label(main, text="🔒 " + self.t("ai.privacy"), style="CardMuted.TLabel", wraplength=900).pack(anchor="w", pady=(8, 0))
        self.image_path = ""
    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if self.image_path: self.task.set(self.t("ai.vision"))
    def send(self):
        prompt = self.input.get("1.0", "end-1c").strip()
        task = self.task_map.get(self.task.get(), "chat")
        if task == "vision": prompt = prompt or "Read the German text in this image, transcribe it, translate it, and explain important spelling or grammar."
        _call_ai(self, prompt, task, self.output, self.image_path if task == "vision" else "")


class SpeakingTab(BaseTab):
    key, subtitle_key = "tab.speaking", "speak.subtitle"
    def build(self):
        self.heading(); main = self.card(); main.pack(fill="both", expand=True)
        bar = ttk.Frame(main, style="Card.TFrame"); bar.pack(fill="x")
        self.scenario = tk.StringVar(value="Im Café")
        ttk.Label(bar, text=self.t("speak.scenario"), style="CardMuted.TLabel").pack(side="left")
        ttk.Combobox(bar, textvariable=self.scenario, state="readonly", values=("Im Café", "Am Bahnhof", "Im Hotel", "Beim Einkaufen", "Beim Arzt"), width=24).pack(side="left", padx=8)
        ttk.Button(bar, text=self.t("speak.begin"), style="Accent.TButton", command=self.begin).pack(side="left")
        self.history = self.text(main, height=14); self.history.pack(fill="both", expand=True, pady=10); self.history.configure(state="disabled")
        row = ttk.Frame(main, style="Card.TFrame"); row.pack(fill="x")
        self.entry = ttk.Entry(row); self.entry.pack(side="left", fill="x", expand=True)
        ttk.Button(row, text=self.t("ai.send"), command=self.reply).pack(side="left", padx=8)
    def begin(self):
        self.entry.delete(0, "end")
        prompt = f"Start a short A1 German role-play in the scenario '{self.scenario.get()}'. Speak as the other person. Ask only one short question."
        _call_ai(self, prompt, "dialogue", self.history)
    def reply(self):
        text = self.entry.get().strip()
        if not text: return
        existing = self.history.get("1.0", "end-1c")
        prompt = f"Scenario: {self.scenario.get()}\nTutor: {existing}\nLearner: {text}\nCorrect gently if needed, then continue with one short German question."
        _call_ai(self, prompt, "dialogue", self.history)


class WritingTab(BaseTab):
    key, subtitle_key = "tab.writing", "write.subtitle"
    def build(self):
        self.heading(); pane = ttk.Panedwindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = self.card(pane); right = self.card(pane); pane.add(left, weight=3); pane.add(right, weight=2)
        ttk.Label(left, text=self.t("write.prompt"), style="CardMuted.TLabel").pack(anchor="w")
        self.input = self.text(left, height=11); self.input.pack(fill="both", expand=True, pady=8)
        ttk.Button(left, text=self.t("write.correct"), style="Accent.TButton", command=self.correct).pack(anchor="e")
        self.output = self.text(left, height=8); self.output.pack(fill="x", pady=(8, 0)); self.output.configure(state="disabled")
        ttk.Label(right, text=self.t("write.canvas"), style="CardMuted.TLabel").pack(anchor="w")
        self.canvas = tk.Canvas(right, bg="#fffdf7", highlightthickness=1, highlightbackground=self.palette["border"], cursor="pencil")
        self.canvas.pack(fill="both", expand=True, pady=8); self.last = None
        self.canvas.bind("<Button-1>", self.down); self.canvas.bind("<B1-Motion>", self.draw); self.canvas.bind("<ButtonRelease-1>", lambda _e: setattr(self, "last", None))
        ttk.Button(right, text=self.t("g.clear"), command=lambda: self.canvas.delete("all")).pack(anchor="e")
    def down(self, event): self.last = (event.x, event.y)
    def draw(self, event):
        if self.last: self.canvas.create_line(*self.last, event.x, event.y, fill="#17233c", width=3, capstyle="round", smooth=True)
        self.last = (event.x, event.y)
    def correct(self):
        prompt = "Correct this German learner text. Show a corrected version, name the grammar rule, and give a brief explanation:\n\n" + self.input.get("1.0", "end-1c")
        _call_ai(self, prompt, "correct", self.output)
