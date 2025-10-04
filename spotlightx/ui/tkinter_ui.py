#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SpotlightX - Sophisticated Linux Application Launcher
# Copyright (c) 2025 WHO-AM-I-404
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Tkinter UI fallback for SpotlightX.
Lightweight UI for development and systems without PySide6.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable, Optional


class TkinterUI:
    def __init__(self, on_query_callback: Callable, on_select_callback: Callable):
        self.on_query = on_query_callback
        self.on_select = on_select_callback
        
        self.root = tk.Tk()
        self.root.title("SpotlightX")
        self.root.attributes('-topmost', True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 700
        window_height = 500
        
        x = (screen_width - window_width) // 2
        y = screen_height // 4
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.root.overrideredirect(True)
        
        self.setup_ui()
        
        self.results = []
        self.selected_index = 0
        
        self.root.bind('<Escape>', lambda e: self.hide())
        self.root.bind('<Return>', lambda e: self.on_enter())
        self.root.bind('<Up>', lambda e: self.navigate(-1))
        self.root.bind('<Down>', lambda e: self.navigate(1))
        
        self.visible = False
    
    def setup_ui(self):
        """Setup UI components."""
        main_frame = tk.Frame(self.root, bg='#1e1e1e', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.search_entry = tk.Entry(
            main_frame,
            font=('Arial', 16),
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            relief=tk.FLAT,
            borderwidth=0
        )
        self.search_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        self.search_entry.insert(0, "Search apps, files, web...")
        self.search_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.search_entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.search_entry.bind('<KeyRelease>', self.on_key_release)
        
        results_frame = tk.Frame(main_frame, bg='#1e1e1e')
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.results_listbox = tk.Listbox(
            results_frame,
            font=('Arial', 11),
            bg='#2d2d2d',
            fg='#ffffff',
            selectbackground='#0078d4',
            selectforeground='#ffffff',
            relief=tk.FLAT,
            borderwidth=0,
            yscrollcommand=scrollbar.set,
            activestyle='none'
        )
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.results_listbox.yview)
        
        self.results_listbox.bind('<Double-Button-1>', lambda e: self.on_enter())
    
    def on_entry_focus_in(self, event):
        """Clear placeholder on focus."""
        if self.search_entry.get() == "Search apps, files, web...":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg='#ffffff')
    
    def on_entry_focus_out(self, event):
        """Restore placeholder if empty."""
        if not self.search_entry.get():
            self.search_entry.insert(0, "Search apps, files, web...")
            self.search_entry.config(fg='#888888')
    
    def on_key_release(self, event):
        """Handle key release in search entry."""
        if event.keysym in ('Up', 'Down', 'Return', 'Escape'):
            return
        
        query = self.search_entry.get()
        if query and query != "Search apps, files, web...":
            results = self.on_query(query)
            self.display_results(results)
        else:
            self.clear_results()
    
    def display_results(self, results: List[Dict[str, Any]]):
        """Display search results."""
        self.results = results
        self.results_listbox.delete(0, tk.END)
        
        for result in results:
            name = result.get('name', 'Unknown')
            subtitle = result.get('subtitle', '')
            display_text = f"{name}"
            if subtitle:
                display_text += f" — {subtitle[:60]}"
            
            self.results_listbox.insert(tk.END, display_text)
        
        if results:
            self.results_listbox.select_set(0)
            self.selected_index = 0
    
    def clear_results(self):
        """Clear results list."""
        self.results = []
        self.results_listbox.delete(0, tk.END)
        self.selected_index = 0
    
    def navigate(self, direction: int):
        """Navigate through results."""
        if not self.results:
            return
        
        self.results_listbox.select_clear(self.selected_index)
        
        self.selected_index = (self.selected_index + direction) % len(self.results)
        
        self.results_listbox.select_set(self.selected_index)
        self.results_listbox.see(self.selected_index)
    
    def on_enter(self):
        """Handle Enter key."""
        if self.results and 0 <= self.selected_index < len(self.results):
            selected_result = self.results[self.selected_index]
            self.on_select(selected_result)
            self.hide()
    
    def show(self):
        """Show the window."""
        if not self.visible:
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            self.search_entry.focus_set()
            self.search_entry.select_range(0, tk.END)
            self.visible = True
    
    def hide(self):
        """Hide the window."""
        if self.visible:
            self.root.withdraw()
            self.visible = False
            self.clear_results()
    
    def toggle(self):
        """Toggle window visibility."""
        if self.visible:
            self.hide()
        else:
            self.show()
    
    def run(self):
        """Run the Tkinter main loop."""
        self.root.withdraw()
        self.root.mainloop()
