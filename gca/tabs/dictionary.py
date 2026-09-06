from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .. import config as C
from .. import dictionary as D
from ..ai_client import AIError
from ..ui import BaseTab


class DictionaryTab(BaseTab):
    """Three-language dictionary (target ↔ English ↔ Turkish): built-in core entries + the user's own entries + cached AI entries.

    The direction selector (setting ``dict_direction``) is ``auto`` or one of :data:`gca.dictionary.DIRECTIONS`; a fixed
    direction searches only its source side. In a ``*2tr`` direction an entry without a Turkish gloss is completed by the AI
    (per the AI policy) and the gloss is written into that entry instead of adding a duplicate."""
    key, subtitle_key = "tab.dictionary", "dict.subtitle"
    MAX_HISTORY = 12
    POLICY_KEYS = {"auto": "dict.ai_auto", "local": "dict.ai_local", "alt": "dict.ai_alt", "off": "dict.ai_off"}
    COLUMNS = ("head", "trans", "tr", "pos", "extra", "src") if D.HAS_TR else ("head", "trans", "pos", "extra", "src")

    def build(self):
        self.heading()
        self.dict = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r.get("source", D.SOURCE_USER),
                                         r.get("example", ""), r.get("tr", "")) for r in self.repos.dictionary.all()])
        self.results = []; self.history = []; self._last_q = ""     # history: (query, direction) pairs, newest first
        self._ai_seq = 0            # bumped by every explicit or quiet search / AI request: older requests may no longer touch the list
        self._ai_pending = None     # sequence number of the AI request in flight, if any
        self._list_direction = self._direction()   # direction code the current list was requested with (may differ from the combobox)
        bar = ttk.Frame(self); bar.pack(fill="x", pady=(0, 6))
        airow = ttk.Frame(self)          # direction + AI policy + provider state live on their own row so the toolbar never overflows
        self.query = tk.StringVar()
        self.entry = ttk.Entry(bar, textvariable=self.query, font=("Segoe UI", 12)); self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _e: self.search()); self.entry.bind("<KeyRelease>", self._on_key)
        ttk.Button(bar, text=self.t("g.search"), style="Accent.TButton", command=self.search).pack(side="left", padx=5)
        self.dir_label = ttk.Label(bar, text="", style="Muted.TLabel", width=9); self.dir_label.pack(side="left", padx=(2, 8))
        ttk.Button(bar, text="🎲 " + self.t("dict.random"), command=self.random_word).pack(side="left")
        ttk.Label(airow, text=self.t("dict.direction"), style="Muted.TLabel").pack(side="left", padx=(0, 4))
        self._direction_labels = {code: (self.t("dict.dir_auto") if code == "auto" else D.direction_text(code)) for code in D.DIRECTIONS}
        self.direction = tk.StringVar(value=self._direction_labels[self._direction()])
        self.direction_box = ttk.Combobox(airow, textvariable=self.direction, state="readonly", width=10, values=[self._direction_labels[c] for c in D.DIRECTIONS])
        self.direction_box.pack(side="left"); self.direction_box.bind("<<ComboboxSelected>>", self._direction_changed)
        ttk.Label(airow, text=self.t("dict.ai_policy"), style="Muted.TLabel").pack(side="left", padx=(14, 4))
        self._policy_labels = {code: self.t(k) for code, k in self.POLICY_KEYS.items()}
        self.policy = tk.StringVar(value=self._policy_labels.get(self.app.settings.get("dict_ai", "auto"), self._policy_labels["auto"]))
        self.policy_box = ttk.Combobox(airow, textvariable=self.policy, state="readonly", width=11, values=[self._policy_labels[c] for c in C.DICT_AI_POLICIES])
        self.policy_box.pack(side="left"); self.policy_box.bind("<<ComboboxSelected>>", self._policy_changed)
        self.ai_state = ttk.Label(airow, text="", style="Muted.TLabel"); self.ai_state.pack(side="left", padx=(8, 0))
        airow.pack(fill="x", pady=(0, 8))
        ttk.Button(bar, text="+ " + self.t("dict.add_entry"), command=self.add_entry).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↓ {self.t('dict.import')}", command=self.import_file).pack(side="right", padx=3)
        ttk.Button(bar, text=f"↑ {self.t('dict.export')}", command=self.export_file).pack(side="right", padx=3)

        pane = ttk.PanedWindow(self, orient="horizontal"); pane.pack(fill="both", expand=True)
        left = ttk.Frame(pane)
        self.tree = ttk.Treeview(left, columns=self.COLUMNS, show="headings", selectmode="browse")
        specs = {"head": (self.t("dict.headword"), 190, False), "trans": (self.t("dict.translation"), 220, True),
                 "tr": (self.t("dict.turkish"), 200, True), "pos": (self.t("words.pos"), 70, False),
                 "extra": (self.t("dict.extra"), 110, False), "src": (self.t("dict.source"), 70, False)}
        for col in self.COLUMNS:
            title, width, stretch = specs[col]
            self.tree.heading(col, text=title); self.tree.column(col, width=width, minwidth=40, anchor="w", stretch=stretch)
        self.tree.configure(displaycolumns=self._columns_for(self._direction()))
        vs = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=vs.set)
        self.tree.pack(side="left", fill="both", expand=True); vs.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.selected); self.tree.bind("<Double-1>", lambda _e: self.speak())
        pane.add(left, weight=3)

        right = self.card(pane); pane.add(right, weight=2)
        self.w_head = ttk.Label(right, text="—", style="Card.TLabel", font=("Segoe UI", 24, "bold"), wraplength=360, justify="left"); self.w_head.pack(anchor="w")
        self.w_meta = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_meta.pack(anchor="w", pady=(4, 0))
        self.w_trans = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 12, "bold"), wraplength=360, justify="left"); self.w_trans.pack(anchor="w", pady=(10, 0))
        self.w_tr = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 12, "bold"), wraplength=360, justify="left")
        if D.HAS_TR: self.w_tr.pack(anchor="w", pady=(2, 0))
        self.w_example = ttk.Label(right, text="", style="Card.TLabel", font=("Segoe UI", 10, "italic"), wraplength=360, justify="left"); self.w_example.pack(anchor="w", pady=(6, 0))
        self.w_note = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_note.pack(anchor="w", pady=(6, 0))
        self.w_bank = ttk.Label(right, text="", style="CardMuted.TLabel", wraplength=360, justify="left"); self.w_bank.pack(anchor="w", pady=(6, 0))
        row1 = ttk.Frame(right, style="Card.TFrame"); row1.pack(anchor="w", pady=(12, 3))
        ttk.Button(row1, text="🔊 " + self.t("pron.speak"), command=self.speak).pack(side="left")
        ttk.Button(row1, text="✦ " + self.t("dict.ask_ai"), command=self.ask_ai).pack(side="left", padx=4)
        ttk.Button(row1, text=self.t("dict.copy"), command=self.copy_entry).pack(side="left")
        row2 = ttk.Frame(right, style="Card.TFrame"); row2.pack(anchor="w", pady=(0, 10))
        ttk.Button(row2, text="★ " + self.t("dict.to_bank"), style="Accent.TButton", command=self.add_to_bank).pack(side="left")
        self.save_btn = ttk.Button(row2, text="💾 " + self.t("dict.save_entry"), command=self.save_ai_entry)   # packed only for unsaved AI entries
        ttk.Label(right, text=self.t("dict.history") + ":", style="CardMuted.TLabel").pack(anchor="w")
        self.hist = tk.Listbox(right, height=5, activestyle="none", relief="flat", highlightthickness=0,
                               bg=self.palette["panel"], fg=self.palette["fg"], font=("Segoe UI", 9))
        self.hist.pack(fill="x"); self.hist.bind("<<ListboxSelect>>", self._pick_history)
        ttk.Label(right, text=self.t("dict.ai_answer") + ":", style="CardMuted.TLabel").pack(anchor="w", pady=(10, 0))
        self.ai_out = self.text(right, height=8); self.ai_out.pack(fill="both", expand=True); self.ai_out.configure(state="disabled")

        self.count_label = ttk.Label(self, text="", style="Muted.TLabel"); self.count_label.pack(anchor="w", pady=(6, 0))
        self._update_count(); self.entry.focus_set(); self.refresh_ai_state()

    # ------------------------------------------------------------------
    def on_show(self):
        """Called by the shell whenever the page is selected: pick up settings changed elsewhere."""
        label = self._policy_labels.get(self.app.settings.get("dict_ai", "auto"))
        if label and label != self.policy.get(): self.policy.set(label)
        label = self._direction_labels[self._direction()]
        if label != self.direction.get(): self.direction.set(label)
        self.refresh_ai_state()

    def _policy_changed(self, _event=None):
        code = next((c for c, label in self._policy_labels.items() if label == self.policy.get()), "auto")
        self.app.settings["dict_ai"] = code; C.save_settings(self.app.settings); self.refresh_ai_state()

    def _direction(self) -> str:
        """The chosen direction code (validated; ``auto`` when the setting is missing or stale)."""
        code = self.app.settings.get("dict_direction", "auto")
        return code if code in D.DIRECTIONS else "auto"

    def _direction_changed(self, _event=None):
        """Combobox handler: persist the choice and re-run the current query in the new direction."""
        code = next((c for c, label in self._direction_labels.items() if label == self.direction.get()), "auto")
        self.app.settings["dict_direction"] = code; C.save_settings(self.app.settings)
        if self.query.get().strip(): self.search()
        else: self.dir_label.configure(text=""); self._list_direction = code; self._fill(code, [])

    def _headword_direction(self) -> str:
        """Direction for looking up a headword the dictionary already contains: the chosen one when it starts from the
        target language (or is automatic), else its mirror - a random word in EN → DE is shown as DE → EN, in TR → DE as DE → TR."""
        chosen = self._direction()
        src, _dst = D.split_direction(chosen)
        return chosen if chosen == "auto" or src == C.TARGET_LANG else D.direction_code(C.TARGET_LANG, src)

    def _columns_for(self, direction: str) -> tuple:
        """Column order: headword | English | Türkçe | … - the Turkish column moves right after the headword for ``*2tr``."""
        if D.HAS_TR and D.target_field(direction) == "tr":
            return ("head", "tr", "trans", "pos", "extra", "src")
        return self.COLUMNS

    def refresh_ai_state(self):
        """Provider status label ("LM Studio: connected" / "Alternative: ready" / "AI off"), probed in the background."""
        if self.app.settings.get("dict_ai", "auto") == "off":
            self.ai_state.configure(text=self.t("dict.state_off")); return
        self.ai_state.configure(text="…")
        def work(): return self.app.dict_provider()
        def done(client):
            if not self.winfo_exists(): return
            key = "dict.state_none" if client is None else ("dict.state_alt" if client is self.app.ai_alt else "dict.state_local")
            self.ai_state.configure(text=self.t(key))
        self.app.run_async(work, done, lambda _exc: self.winfo_exists() and self.ai_state.configure(text=self.t("dict.state_none")))

    def _update_count(self):
        by = self.dict.count_by_source()
        self.count_label.configure(text=f"{len(self.dict)} {self.t('dict.entries')}  ·  {self.t('dict.builtin')} {by.get(D.SOURCE_BUILTIN, 0)}"
                                        f"  ·  {self.t('dict.user')} {by.get(D.SOURCE_USER, 0)}  ·  {self.t('dict.ai_source')} {by.get(D.SOURCE_AI, 0)}")

    def _on_key(self, event):
        q = self.query.get().strip()
        if not q: self._last_q = ""; self.dir_label.configure(text=""); self._list_direction = self._direction(); self._fill(self._list_direction, []); return
        if q == self._last_q or event.keysym in ("Return", "Up", "Down"): return     # modifier/cursor keys: the text did not change
        if len(q) >= 2: self.search(quiet=True)

    def search(self, quiet: bool = False, direction: str | None = None):
        """Look the query up in ``direction`` (default: the chosen one) and, unless ``quiet``, remember it and ask the AI when needed."""
        q = self.query.get().strip()
        if not q: return
        direction = direction or self._direction()
        self._last_q = q; self._ai_seq += 1                  # the list now belongs to this query; an older AI answer is still cached, just not listed
        rows = self._list(q, direction)
        if quiet: return
        self._remember(q, direction)
        if rows:
            self._select_first()
            self.app.status.set(f"'{q}': {len(rows)} {self.t('dict.results')}")
            if self._turkish_missing(rows, direction) and self.app.settings.get("dict_ai", "auto") != "off":
                self._run_ai(q, merge=True); self.app.status.set(self.t("dict.tr_missing"))
        else:
            self.app.status.set(self.t("dict.no_result")); self._write_ai(self.t("dict.no_result"))
            if self.app.settings.get("dict_ai", "auto") != "off": self._run_ai(q, merge=False)

    @staticmethod
    def _turkish_missing(rows: list, direction: str) -> bool:
        """True when a fixed ``*2tr`` search found an entry whose Turkish gloss is still unknown (the AI can fill it)."""
        return D.HAS_TR and direction != "auto" and D.target_field(direction) == "tr" and bool(rows) and not rows[0].tr

    def _list(self, q: str, direction: str | None = None) -> list:
        """Local lookup shown in the tree together with the effective direction label; returns the rows."""
        self._list_direction = direction or self._direction()
        direction, rows = self.dict.lookup(q, self._list_direction)
        self._fill(direction, rows)
        self.dir_label.configure(text=D.direction_text(direction))
        return rows

    def _relist(self):
        """Show the current text afresh in the direction of the current list (entries gained a Turkish gloss meanwhile)."""
        q = self.query.get().strip()
        if q: self._list(q, self._list_direction); self._select_first()

    def _relist_if_stale(self):
        """Re-list only when a listed stored row no longer is the dictionary's object for its key (a superseded AI answer filled
        its gloss): unsaved "Ask AI" rows of a newer query are left alone."""
        if any(e.source != D.SOURCE_AI and self.dict.twin(e) is not e for e in self.results): self._relist()

    def _fill(self, direction, rows):
        for item in self.tree.get_children(): self.tree.delete(item)
        self.tree.configure(displaycolumns=self._columns_for(direction))
        if D.HAS_TR: self.w_tr.pack_configure(**({"before": self.w_trans} if D.target_field(direction) == "tr" else {"after": self.w_trans}))
        self.results = rows; lang = self.app.ui_lang
        names = {D.SOURCE_BUILTIN: self.t("dict.builtin"), D.SOURCE_USER: self.t("dict.user"), D.SOURCE_AI: self.t("dict.ai_source")}
        for i, e in enumerate(rows):
            extra = e.plural if e.pos == "n" and C.TARGET_LANG == "de" else e.extra
            values = {"head": e.display, "trans": e.translation, "tr": e.tr or "—", "pos": e.pos_label(lang), "extra": extra, "src": names.get(e.source, e.source)}
            self.tree.insert("", "end", iid=str(i), values=tuple(values[c] for c in self.COLUMNS))

    def _select_first(self):
        children = self.tree.get_children()
        if children: self.tree.selection_set(children[0]); self.tree.focus(children[0]); self.selected()

    def _remember(self, q, direction):
        """Keep (query, direction) so that a history pick re-runs the lookup exactly as it was, whatever the combobox says now."""
        self.history = [(h, d) for h, d in self.history if h != q]
        self.history.insert(0, (q, direction)); del self.history[self.MAX_HISTORY:]
        self.hist.delete(0, "end")
        for h, _d in self.history: self.hist.insert("end", h)

    def _pick_history(self, _event=None):
        """Re-run a remembered lookup in its own direction; when that side no longer finds anything (the query was last
        re-run after a direction switch), fall back to automatic detection instead of repeating a dead end and asking the AI."""
        sel = self.hist.curselection()
        if not sel or sel[0] >= len(self.history): return
        q, direction = self.history[sel[0]]
        if direction != "auto" and not self.dict.lookup(q, direction)[1]: direction = "auto"
        self.query.set(q); self.search(direction=direction)

    def current(self):
        sel = self.tree.selection()
        if not sel: return None
        try: return self.results[int(sel[0])]
        except (ValueError, IndexError): return None

    def selected(self, _event=None):
        e = self.current()
        if not e: return
        lang = self.app.ui_lang
        self.w_head.configure(text=e.display)
        meta = e.pos_label(lang)
        if e.pos == "n" and e.gender:
            art = {"de": e.extra.split()[0] if e.extra.split() else "", "fr": {"m": "le", "f": "la", "pl": "les", "mf": "le/la"}.get(e.gender, "")}.get(C.TARGET_LANG, "")
            meta += f" · {self.t('words.gender')}: {e.gender}" + (f" ({art})" if art else "")
        if e.plural: meta += f" · {self.t('words.plural')}: {e.plural}"
        elif e.extra and e.pos != "n": meta += f" · {e.extra}"
        if e.source == D.SOURCE_AI: meta += f" · {self.t('dict.ai_source')}"
        self.w_meta.configure(text=meta)
        self.w_trans.configure(text=f"{self.t('dict.translation')}: {e.translation}")
        if D.HAS_TR: self.w_tr.configure(text=f"{self.t('dict.turkish')}: {e.tr or '—'}")
        self.w_example.configure(text=f"„{e.example}“" if e.example else "")
        self.w_note.configure(text=e.note)
        hits = [w for w in self.repos.words.search(e.headword, limit=5) if C.normalize_search(w["target"]) == C.normalize_search(e.headword)]
        self.w_bank.configure(text=f"★ {self.t('tab.words')}: {hits[0]['tr']} ({hits[0]['deck']})" if hits else "")
        if e.source == D.SOURCE_AI and self.dict.would_change(e): self.save_btn.pack(side="left", padx=4)
        else: self.save_btn.pack_forget()

    # ------------------------------------------------------------------
    def speak(self):
        e = self.current()
        if e: self.app.speak(e.headword)

    def random_word(self):
        """A random built-in headword, looked up on the headword side whatever the chosen direction (EN → DE / TR → DE would
        search the other language, find nothing and needlessly ask the AI for a word the dictionary already knows)."""
        e = self.dict.random_entry()
        if e: self.query.set(e.headword); self.search(direction=self._headword_direction())

    def copy_entry(self):
        e = self.current()
        if not e: return
        self.clipboard_clear(); self.clipboard_append(f"{e.display} — {e.translation}" + (f" — {e.tr}" if e.tr else "")); self.app.status.set(self.t("dict.copied"))

    def add_to_bank(self):
        """The word bank's ``tr`` field gets the first Turkish sense when the entry has one, else the first translation sense (old behaviour)."""
        e = self.current()
        if not e: return
        first = e.translation.split(";")[0].strip()
        turkish = e.tr.split(";")[0].strip() if e.tr else ""
        fields = {"pos": e.pos, "deck": self.t("tab.dictionary"), "example_target": e.example, "example_en": e.note if C.TARGET_LANG == "en" else ""}
        if C.TARGET_LANG == "de" and e.pos == "n":
            art = e.extra.split()[0] if e.extra.split() else ""
            fields.update(article=art, gender={"der": "masculine", "die": "feminine", "das": "neuter"}.get(art, ""), plural=e.plural)
        elif C.TARGET_LANG == "fr" and e.pos == "n":
            fields.update(gender={"m": "masculin", "f": "féminin", "mf": "masculin/féminin", "pl": "pluriel"}.get(e.gender, ""), plural=e.plural,
                          article={"m": "le", "f": "la", "pl": "les"}.get(e.gender, ""))
        if C.TARGET_LANG == "en": self.repos.words.add(e.headword, first, e.headword, **fields)
        else: self.repos.words.add(e.headword, turkish or first, e.translation, **fields)
        self.app.status.set(f"{self.t('dict.added_bank')}: {e.headword}"); self.selected()

    # ------------------------------------------------------------------ AI
    def ask_ai(self):
        """Explicit lookup: AI entries are merged on top of whatever the local dictionary found (listed, not autosaved)."""
        e = self.current(); text = self.query.get().strip() or (e.headword if e else "")
        if not text: return
        if self.app.settings.get("dict_ai", "auto") == "off":
            self._write_ai(self.t("ai.status_off")); return
        self._run_ai(text, merge=True)

    def _model_for(self, client) -> str:
        return self.app.settings.get("alt_model" if client is self.app.ai_alt else "ai_model", "") or ""

    def _run_ai(self, q: str, merge: bool):
        self._ai_seq += 1; seq = self._ai_seq; self._ai_pending = seq
        self._write_ai(self.t("dict.ai_asking")); self.app.status.set(self.t("dict.ai_asking"))
        def work():
            client = self.app.dict_provider()
            if client is None: return client, None
            return client, D.ai_lookup(client, q, self.app.ui_lang, self._model_for(client))
        def done(result):
            if not self.winfo_exists(): return
            client, entries = result
            filled, used = [], []
            if entries and self.app.settings.get("dict_ai_autosave", True):          # cached / filled even when superseded
                filled, used = self._fill_turkish(entries)
                if not merge: self._autosave(entries, seq)
                if filled and seq != self._ai_seq: self._relist_if_stale()           # the list (and self.results) must show the stored gloss
            if client is None: self._finish(seq, self.t("ai.status_off"), self.t("ai.status_off")); return
            self._show_ai_entries(seq, q, entries, client, merge, filled, used)
        def error(exc):
            if not self.winfo_exists(): return
            text = f"{self.t('ai.status_off')}\n\n({exc})" if isinstance(exc, AIError) else self.t("ai.status_off")
            if self._finish(seq, text, self.t("ai.status_off")): self.refresh_ai_state()
        self.app.run_async(work, done, error)

    def _finish(self, seq: int, text: str, status: str) -> bool:
        """Report the outcome of AI request ``seq``; True when it is still the current one.

        A superseded request (the user searched on meanwhile) leaves the list alone, but it must not leave
        "asking…" on screen either - unless a newer request is running and owns that text."""
        if self._ai_pending == seq: self._ai_pending = None
        if seq == self._ai_seq:
            self._write_ai(text); self.app.status.set(status); return True
        if self._ai_pending is None:
            asking = {self.t("dict.ai_asking"), self.t("dict.tr_missing")}
            if self.ai_out.get("1.0", "end").strip() in asking: self._write_ai(text)
            if self.app.status.get() in asking: self.app.status.set(status)
        return False

    def _ai_direction(self, q: str, entries: list) -> str:
        """Direction label for an AI answer: the list's fixed direction, else which side of the answer the query matched."""
        chosen = self._list_direction
        if chosen != "auto": return chosen
        qn = C.normalize_search(q)
        if qn in {C.normalize_search(e.headword) for e in entries}: return D.DEFAULT_DIRECTION
        if any(qn in D._senses(e.translation) for e in entries): return D.direction_code(D.OTHER_LANG, C.TARGET_LANG)   # "to procrastinate" -> aufschieben
        if D.HAS_TR and any(qn in D._senses(e.tr) for e in entries): return D.direction_code("tr", C.TARGET_LANG)
        return self.dict.lookup(q)[0]

    def _show_ai_entries(self, seq: int, q: str, entries: list, client, merge: bool, filled: list = (), used: list = ()):
        provider = f"{self.app.provider_name(client)} · {getattr(client, 'last_model', '') or self._model_for(client)}"
        if not entries:
            self._finish(seq, f"{self.t('dict.ai_none')}\n\n— {self.t('dict.answered_by')}: {provider}", self.t("dict.ai_none")); return
        lang = self.app.ui_lang; lines = []
        for e in entries:
            head = e.display + (f"  ({e.extra})" if e.extra and not (e.pos == "n" and C.TARGET_LANG == "de") else (f"  ({e.plural})" if e.plural else ""))
            lines.append(f"• {head}  [{e.pos_label(lang)}]\n    {self.t('dict.translation')}: {e.translation}")
            if D.HAS_TR: lines.append(f"    {self.t('dict.turkish')}: {e.tr or '—'}")
            if e.example: lines.append(f"    „{e.example}“")
            if e.note: lines.append(f"    ({e.note})")
        lines.append(f"\n— {self.t('dict.answered_by')}: {provider}")
        status = f"{self.t('dict.tr_filled')}: {', '.join(e.headword for e in filled)}" if filled else f"'{q}': {len(entries)} {self.t('dict.ai_results')}"
        if not self._finish(seq, "\n".join(lines), status): return
        if filled:      # existing entries gained their Turkish gloss: list them afresh, keep only genuinely new AI entries on top
            direction, local = self.dict.lookup(q, self._list_direction)
            rows = [e for e in entries if e not in used and not self.dict.contains(e)] + local
        else:
            direction = self._ai_direction(q, entries)
            rows = entries + ([e for e in self.results if e.source != D.SOURCE_AI] if merge else [])
        self._fill(direction, rows)
        self.dir_label.configure(text=D.direction_text(direction))
        self._select_first()

    def _fill_turkish(self, entries: list) -> tuple[list, list]:
        """Existing entries get Turkish senses from a matching AI answer - in memory and in SQLite - so the dictionary never
        grows a duplicate just to carry the Turkish side. Returns ``(filled, used)``: the updated stored entries and the AI
        answers that were merged into them (those need no row of their own in the list).

        An answer with an exact twin (headword, pos, translation) extends that twin's gloss; those are handled first so that
        the exact match wins. Without a twin, only same-headword entries that still lack a gloss *and* share an English sense
        with the answer are filled: ``Schloss`` = castle must never receive the gloss of ``Schloss`` = lock."""
        if not D.HAS_TR: return [], []
        filled, used = [], []
        for a in sorted((a for a in entries if a.tr), key=lambda a: self.dict.twin(a) is None):
            twin = self.dict.twin(a)
            if twin is not None:
                targets = [twin] if self.dict.would_change(a) else []
            else:
                senses = set(D._senses(a.translation))
                targets = [e for e in self.dict.find(a.headword, a.pos) if not e.tr and senses & set(D._senses(e.translation))]
            for e in targets:
                self._persist([D.Entry(e.headword, e.pos, e.extra, e.translation, e.note, D.SOURCE_AI, e.example, a.tr)])
                filled.append(self.dict.twin(e))
            if targets: used.append(a)
        return filled, used

    def _autosave(self, entries: list, seq: int) -> int:
        """Cache a fallback answer, skipping headwords the dictionary already knows (near-duplicates of built-in, user or
        earlier AI entries stay listed with a "Save" button instead). When the answer was superseded while the user kept
        typing and the list is empty, it is refreshed so the freshly cached entries can show up for the current text."""
        fresh = [e for e in entries if not self.dict.has_headword(e.headword, e.pos)]
        added = self._persist(fresh) if fresh else 0
        if added and seq != self._ai_seq and not self.tree.get_children():
            q = self.query.get().strip()
            if q: self._list(q, self._list_direction)
        return added

    def _persist(self, entries: list) -> int:
        """Store AI entries in SQLite and in the in-memory dictionary; returns how many were new to the dictionary.

        An entry whose twin is already stored only contributes Turkish senses (:meth:`gca.dictionary.Dictionary.merge_tr`):
        the stored row is updated in place, or, for a built-in twin without a row, an ``ai`` row carrying the gloss is
        stored and merged into the built-in entry on the next start. A twin that gains nothing is left alone."""
        rows = []
        for e in entries:
            twin = self.dict.twin(e)
            if twin is not None:
                tr = self.dict.merge_tr(twin, e)
                if tr == twin.tr or self.repos.dictionary.set_tr(twin.headword, twin.translation, tr): continue
            rows.append((e.headword, e.translation, e.pos, e.extra, e.note, e.example, e.tr))
        if rows: self.repos.dictionary.add_many(rows, D.SOURCE_AI)
        added = self.dict.extend(entries); self._update_count(); return added

    def save_ai_entry(self):
        e = self.current()
        if not e or e.source != D.SOURCE_AI: return
        merged = self.dict.contains(e)                      # an exact twin exists: saving only adds the Turkish senses to it
        self._persist([e]); self.app.status.set(f"{self.t('dict.ai_saved')}: {e.headword}")
        if merged and self.query.get().strip(): self._relist()
        else: self.selected()

    def _write_ai(self, text):
        self.ai_out.configure(state="normal"); self.ai_out.delete("1.0", "end"); self.ai_out.insert("1.0", text); self.ai_out.configure(state="disabled")

    # ------------------------------------------------------------------
    def add_entry(self):
        dlg = tk.Toplevel(self); dlg.title(self.t("dict.add_entry")); dlg.configure(background=self.palette["bg"]); dlg.transient(self.app); dlg.grab_set()
        fields = {}
        q = self.query.get().strip(); src = D.source_field(self.dict.lookup(q, self._direction())[0]) if q else ""
        specs = [("headword", self.t("dict.headword"), q if src == "headword" else ""),
                 ("translation", self.t("dict.translation"), q if src == "translation" else "")]
        if D.HAS_TR: specs.append(("tr", self.t("dict.turkish"), q if src == "tr" else ""))
        specs += [("pos", self.t("words.pos") + " (n/v/adj/…)", ""), ("extra", self.t("dict.extra"), ""), ("note", self.t("dict.note"), ""),
                  ("example", self.t("dict.example"), "")]
        for i, (key, label, value) in enumerate(specs):
            ttk.Label(dlg, text=label).grid(row=i, column=0, sticky="w", padx=12, pady=5)
            var = tk.StringVar(value=value); ttk.Entry(dlg, textvariable=var, width=40).grid(row=i, column=1, padx=12, pady=5); fields[key] = var
        def save():
            head, trans = fields["headword"].get().strip(), fields["translation"].get().strip()
            if not head or not trans: messagebox.showwarning(C.APP_NAME, self.t("dict.required"), parent=dlg); return
            pos, extra, note, example = (fields[k].get().strip() for k in ("pos", "extra", "note", "example"))
            tr = fields["tr"].get().strip() if "tr" in fields else ""
            self.repos.dictionary.add(head, trans, pos, extra, note, D.SOURCE_USER, example, tr)
            self.dict.extend([D.Entry(head, pos, extra, trans, note, D.SOURCE_USER, example, tr)])
            dlg.destroy(); self._update_count(); self.query.set(head); self.search()
        ttk.Button(dlg, text=self.t("g.save"), style="Accent.TButton", command=save).grid(row=len(specs), column=1, sticky="e", padx=12, pady=12)
        dlg.bind("<Return>", lambda _e: save()); dlg.bind("<Escape>", lambda _e: dlg.destroy())

    def import_file(self):
        path = filedialog.askopenfilename(title=self.t("dict.import"), filetypes=[("CSV / TSV", "*.csv *.tsv *.txt"), ("*", "*.*")])
        if not path: return
        try: entries = D.read_table(Path(path))
        except Exception as exc: messagebox.showerror(C.APP_NAME, str(exc), parent=self); return
        n = self.repos.dictionary.add_many([(e.headword, e.translation, e.pos, e.extra, e.note, e.example, e.tr) for e in entries], D.SOURCE_USER)
        self.dict.extend(entries); self._update_count(); self.app.status.set(f"{n} {self.t('dict.imported')}")

    def export_file(self):
        path = filedialog.asksaveasfilename(title=self.t("dict.export"), defaultextension=".csv", initialdir=str(C.EXPORT_DIR),
                                            initialfile=f"dictionary_{C.TARGET_LANG}.csv", filetypes=[(self.t("words.csv"), "*.csv")])
        if not path: return
        n = D.write_table(Path(path), self.results or self.dict.entries); self.app.status.set(f"{n} {self.t('dict.exported')}")
