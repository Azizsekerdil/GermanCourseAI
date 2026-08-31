from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from . import config as C
from .ai_client import AIClient
from .db import Database, Repos
from .i18n import LANG_NAMES, t
from .tts import Speaker
from .ui import FONT, apply_theme
from .tabs.learning import ExamTab, StudyTab, WordsTab
from .tabs.labs import GrammarTab, OrthographyTab, PronunciationTab
from .tabs.reading import LibraryTab, PDFTab, ResourcesTab
from .tabs.practice import AITab, SpeakingTab, WritingTab
from .tabs.system import GuideTab, PacksTab, ProgressTab, SettingsTab, TokensTab

TAB_SPECS = [
    ("tab.study", StudyTab, "↻", "grp.learn"), ("tab.words", WordsTab, "Aa", "grp.learn"),
    ("tab.exam", ExamTab, "✓", "grp.learn"), ("tab.orthography", OrthographyTab, "Äß", "grp.lab"),
    ("tab.pronunciation", PronunciationTab, "◖", "grp.lab"), ("tab.grammar", GrammarTab, "§", "grp.lab"),
    ("tab.resources", ResourcesTab, "◇", "grp.read"), ("tab.pdf", PDFTab, "▤", "grp.read"),
    ("tab.library", LibraryTab, "▣", "grp.read"), ("tab.ai", AITab, "✦", "grp.practice"),
    ("tab.speaking", SpeakingTab, "◌", "grp.practice"), ("tab.writing", WritingTab, "✎", "grp.practice"),
    ("tab.progress", ProgressTab, "↗", "grp.system"), ("tab.packs", PacksTab, "⬡", "grp.system"),
    ("tab.tokens", TokensTab, "#", "grp.system"), ("tab.guide", GuideTab, "?", "grp.system"),
    ("tab.settings", SettingsTab, "⚙", "grp.system"),
]


class App(tk.Tk):
    def __init__(self):
        super().__init__(); C.ensure_dirs(); self.settings = C.load_settings(); self.ui_lang = self.settings["ui_lang"]
        self.title(f"{C.APP_NAME} {C.VERSION}"); self.geometry("1360x860"); self.minsize(1080, 700)
        try: self.iconbitmap(default=str(C.PROGRAM_DIR / "assets" / "app.ico"))
        except Exception: pass
        self.style = ttk.Style(self); self.palette = apply_theme(self, self.style, self.settings["theme"])
        self.db = Database(); self.repos = Repos(self.db); self.profile_id = self._profile_id()
        self.speaker = Speaker(int(self.settings.get("tts_rate", 155)))
        self.ai = AIClient(self.settings.get("ai_base"), self._log_tokens)
        self._tabs = {}; self.nav_buttons = {}; self._current_key = "tab.study"; self._tasks = queue.Queue()
        self._build_shell(); self.rebuild_navigation(); self.rebuild_pages(); self.select("tab.study")
        self.protocol("WM_DELETE_WINDOW", self.on_close); self.after(80, self._drain_tasks); self.after(600, self.check_ai)

    def t(self, key): return t(key, self.ui_lang)
    def answer_equal(self, given, expected): return C.answer_equal(given, expected)

    def _profile_id(self):
        known = {p["id"] for p in self.repos.profiles.all()}; pid = self.settings.get("profile_id")
        if pid not in known: pid = self.repos.profiles.ensure_default()
        self.settings["profile_id"] = pid; C.save_settings(self.settings); return int(pid)

    def _build_shell(self):
        self.sidebar = tk.Frame(self, width=238, bg=self.palette["deep"]); self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)
        self.side_header = tk.Frame(self.sidebar, bg=self.palette["deep"], height=86); self.side_header.pack(fill="x"); self.side_header.pack_propagate(False)
        tk.Label(self.side_header, text=C.APP_NAME.replace(" AI", "").upper(), bg=self.palette["deep"], fg=self.palette["fg"], font=(FONT, 14, "bold")).pack(anchor="w", padx=18, pady=(18, 0))
        tk.Label(self.side_header, text="AI  ·  " + C.VERSION, bg=self.palette["deep"], fg=self.palette["accent"], font=(FONT, 9, "bold")).pack(anchor="w", padx=18, pady=2)
        self.nav = tk.Frame(self.sidebar, bg=self.palette["deep"]); self.nav.pack(fill="both", expand=True)
        self.right = ttk.Frame(self); self.right.pack(side="left", fill="both", expand=True)
        self.top = tk.Frame(self.right, bg=self.palette["panel"], height=58); self.top.pack(fill="x"); self.top.pack_propagate(False)
        self.page_title = tk.Label(self.top, text="", bg=self.palette["panel"], fg=self.palette["fg"], font=(FONT, 14, "bold")); self.page_title.pack(side="left", padx=20)
        self.ai_status = tk.Label(self.top, text="AI: …", bg=self.palette["card"], fg=self.palette["muted"], font=(FONT, 9), padx=10, pady=5); self.ai_status.pack(side="right", padx=(5, 16))
        self.profile_var = tk.StringVar(); self.profile_box = ttk.Combobox(self.top, textvariable=self.profile_var, state="readonly", width=15); self.profile_box.pack(side="right", padx=5); self.profile_box.bind("<<ComboboxSelected>>", self.change_profile)
        ttk.Button(self.top, text="+", width=3, command=self.new_profile).pack(side="right")
        self.language_var = tk.StringVar(value=LANG_NAMES[self.ui_lang]); self.language_box = ttk.Combobox(self.top, textvariable=self.language_var, state="readonly", width=10,
                                                                                                         values=[LANG_NAMES[x] for x in C.UI_LANGS]); self.language_box.pack(side="right", padx=10)
        self.language_box.bind("<<ComboboxSelected>>", self.language_changed)
        tk.Label(self.top, text="🌐", bg=self.palette["panel"], fg=self.palette["muted"]).pack(side="right")
        self.content = ttk.Frame(self.right, padding=(20, 16, 20, 12)); self.content.pack(fill="both", expand=True)
        self.status = tk.StringVar(value=self.t("g.ready")); self.statusbar = tk.Label(self.right, textvariable=self.status, bg=self.palette["deep"], fg=self.palette["muted"], anchor="w", padx=16, font=(FONT, 9)); self.statusbar.pack(fill="x", side="bottom")
        self.refresh_profiles()

    def rebuild_navigation(self):
        for child in self.nav.winfo_children(): child.destroy()
        self.nav_buttons = {}; current_group = None
        for key, _cls, icon, group in TAB_SPECS:
            if group != current_group:
                current_group = group; tk.Label(self.nav, text=self.t(group), bg=self.palette["deep"], fg=self.palette["muted"], font=(FONT, 8, "bold"), anchor="w").pack(fill="x", padx=18, pady=(10, 3))
            button = tk.Button(self.nav, text=f"{icon:>2}   {self.t(key)}", anchor="w", relief="flat", bd=0,
                               bg=self.palette["deep"], fg=self.palette["fg"], activebackground=self.palette["hover"], activeforeground=self.palette["fg"],
                               font=(FONT, 9), padx=14, pady=5, command=lambda k=key: self.select(k))
            button.pack(fill="x", padx=8); self.nav_buttons[key] = button

    def rebuild_pages(self):
        for page in self._tabs.values(): page.destroy()
        self._tabs = {key: cls(self.content, self) for key, cls, _icon, _group in TAB_SPECS}

    def select(self, key):
        for page in self._tabs.values(): page.pack_forget()
        for k, button in self.nav_buttons.items(): button.configure(bg=self.palette["card"] if k == key else self.palette["deep"], fg=self.palette["accent"] if k == key else self.palette["fg"])
        self._current_key = key; self._tabs[key].pack(fill="both", expand=True); self.page_title.configure(text=self.t(key)); self.status.set(self.t("g.ready"))

    def current_page(self): return self._tabs.get(self._current_key)
    def language_changed(self, _event=None):
        reverse = {name: code for code, name in LANG_NAMES.items()}; self.set_ui_language(reverse.get(self.language_var.get(), "tr"))
    def set_ui_language(self, code):
        if code not in C.UI_LANGS: return
        self.ui_lang = code; self.settings["ui_lang"] = code; C.save_settings(self.settings); self.language_var.set(LANG_NAMES[code])
        current = self._current_key; self.rebuild_navigation(); self.rebuild_pages(); self.select(current); self.refresh_profiles()

    def refresh_profiles(self):
        self.profiles = self.repos.profiles.all(); self.profile_box.configure(values=[p["name"] for p in self.profiles])
        current = next((p["name"] for p in self.profiles if p["id"] == self.profile_id), self.profiles[0]["name"]); self.profile_var.set(current)
    def new_profile(self):
        name = simpledialog.askstring(C.APP_NAME, self.t("g.name"), parent=self)
        if name:
            self.profile_id = self.repos.profiles.create(name); self.settings["profile_id"] = self.profile_id; C.save_settings(self.settings); self.refresh_profiles(); self.rebuild_pages(); self.select(self._current_key)
    def change_profile(self, _event=None):
        found = next((p for p in self.profiles if p["name"] == self.profile_var.get()), None)
        if found:
            self.profile_id = int(found["id"]); self.settings["profile_id"] = self.profile_id; C.save_settings(self.settings); self.rebuild_pages(); self.select(self._current_key)

    def speak(self, text):
        if self.settings.get("tts_enabled"): self.speaker.speak(text)
    def _log_tokens(self, model, task, ptok, ctok, ms, ok):
        self.repos.tokens.log(model, task, ptok, ctok, ms, ok)
    def check_ai(self):
        def work(): return self.ai.available()
        def done(ok): self.ai_status.configure(text="AI: " + (self.t("g.available") if ok else self.t("g.unavailable")), fg=self.palette["ok"] if ok else self.palette["muted"])
        self.run_async(work, done)
    def run_async(self, fn, done=lambda _x: None, error=lambda _e: None):
        def runner():
            try: self._tasks.put((done, fn()))
            except Exception as exc: self._tasks.put((error, exc))
        threading.Thread(target=runner, daemon=True).start()
    def _drain_tasks(self):
        try:
            while True:
                callback, value = self._tasks.get_nowait(); callback(value)
        except queue.Empty: pass
        if self.winfo_exists(): self.after(80, self._drain_tasks)

    def apply_theme_and_rebuild(self):
        self.palette = apply_theme(self, self.style, self.settings["theme"])
        for child in list(self.winfo_children()): child.destroy()
        self._tabs = {}; self._build_shell(); self.rebuild_navigation(); self.rebuild_pages(); self.select(self._current_key)

    def on_close(self):
        try: C.save_settings(self.settings); self.db.close()
        finally: self.destroy()


def main() -> int:
    app = App(); app.mainloop(); return 0
