#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SpotlightX - Enhanced Tkinter UI (Glass Edition)
# Copyright (c) 2025 WHO-AM-I-404
#
# Lightweight “glass-style” UI for SpotlightX launcher.
# Uses pure Tkinter — no heavy dependencies required.

import tkinter as tk
from typing import List, Dict, Any, Callable
import threading
import time


class TkinterUI:
    def __init__(self, on_query_callback: Callable, on_select_callback: Callable):
        self.on_query = on_query_callback
        self.on_select = on_select_callback

        # 🌟 Root window setup
        self.root = tk.Tk()
        self.root.title("SpotlightX")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)  # borderless

        # 💎 Try to apply transparency (if supported)
        try:
            self.root.attributes('-alpha', 0.95)
        except tk.TclError:
            pass

        # 🎨 Geometry setup
        w, h = 700, 500
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x, y = (sw - w) // 2, sh // 4
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        # ⚙️ State variables
        self.results = []
        self.selected_index = 0
        self.visible = False

        # 🧱 Build UI components
        self._build_interface()

        # ⌨️ Key bindings
        self.root.bind('<Escape>', lambda e: self.hide())
        self.root.bind('<Return>', lambda e: self._on_enter())
        self.root.bind('<Up>', lambda e: self._navigate(-1))
        self.root.bind('<Down>', lambda e: self._navigate(1))

    # --------------------------
    # UI Building
    # --------------------------

    def _build_interface(self):
        """Setup the main interface."""
        main = tk.Frame(self.root, bg='#1e1e1e', padx=10, pady=10)
        main.pack(fill=tk.BOTH, expand=True)

        # 🔍 Search bar
        self.entry = tk.Entry(
            main,
            font=('Segoe UI', 16),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            borderwidth=0
        )
        self.entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        self.entry.insert(0, "Search apps, files, web...")
        self.entry.config(fg='#888888')
        self.entry.bind('<FocusIn>', self._focus_in)
        self.entry.bind('<FocusOut>', self._focus_out)
        self.entry.bind('<KeyRelease>', self._on_key)

        # 📜 Results frame
        result_frame = tk.Frame(main, bg='#1e1e1e')
        result_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            result_frame,
            font=('Segoe UI', 11),
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#0078d4',
            selectforeground='#ffffff',
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set,
            activestyle='none'
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<Double-Button-1>', lambda e: self._on_enter())

    # --------------------------
    # Input / Query Handling
    # --------------------------

    def _focus_in(self, _):
        if self.entry.get() == "Search apps, files, web...":
            self.entry.delete(0, tk.END)
            self.entry.config(fg='#ffffff')

    def _focus_out(self, _):
        if not self.entry.get().strip():
            self.entry.insert(0, "Search apps, files, web...")
            self.entry.config(fg='#888888')

    def _on_key(self, event):
        if event.keysym in ('Up', 'Down', 'Return', 'Escape'):
            return
        query = self.entry.get().strip()
        if query and query != "Search apps, files, web...":
            results = self.on_query(query)
            self._show_results(results)
        else:
            self._clear_results()

    def _show_results(self, results: List[Dict[str, Any]]):
        self.results = results
        self.listbox.delete(0, tk.END)

        for res in results:
            name = res.get('name', 'Unknown')
            subtitle = res.get('subtitle', '')
            text = f"{name}"
            if subtitle:
                text += f" — {subtitle[:60]}"
            self.listbox.insert(tk.END, text)

        if results:
            self.listbox.select_set(0)
            self.selected_index = 0

    def _clear_results(self):
        self.results = []
        self.listbox.delete(0, tk.END)
        self.selected_index = 0

    def _navigate(self, direction: int):
        if not self.results:
            return
        self.listbox.select_clear(self.selected_index)
        self.selected_index = (self.selected_index + direction) % len(self.results)
        self.listbox.select_set(self.selected_index)
        self.listbox.see(self.selected_index)

    def _on_enter(self):
        if self.results and 0 <= self.selected_index < len(self.results):
            selected = self.results[self.selected_index]
            self.on_select(selected)
            self.hide()

    # --------------------------
    # Window Show/Hide Logic
    # --------------------------

    def show(self):
        if not self.visible:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.entry.focus_set()
            self.entry.select_range(0, tk.END)
            self._fade_in()
            self.visible = True

    def hide(self):
        if self.visible:
            self._fade_out()
            self.visible = False
            self._clear_results()

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    # --------------------------
    # Simple Fade Animations
    # --------------------------

    def _fade_in(self):
        def _animate():
            for alpha in range(0, 96, 5):
                try:
                    self.root.attributes('-alpha', alpha / 100)
                    time.sleep(0.01)
                except tk.TclError:
                    break
        threading.Thread(target=_animate, daemon=True).start()

    def _fade_out(self):
        def _animate():
            for alpha in range(95, -1, -5):
                try:
                    self.root.attributes('-alpha', alpha / 100)
                    time.sleep(0.01)
                except tk.TclError:
                    break
            self.root.withdraw()
        threading.Thread(target=_animate, daemon=True).start()

    # --------------------------
    # Loop
    # --------------------------

    def run(self):
        self.root.withdraw()
        self.root.mainloop()
