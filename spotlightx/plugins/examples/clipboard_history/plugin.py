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
Clipboard History Plugin for SpotlightX
Stores recent clipboard entries and allows pasting them.
"""

import pyperclip
import time
import json
from pathlib import Path


class ClipboardHistory:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.max_items = 50
        self.history = []
        self.last_clipboard = ""
        
        config_dir = self.pm.get_plugin_config_dir('clipboard_history')
        self.history_file = config_dir / 'history.json'
        
        self.load_history()
    
    def load_history(self):
        """Load clipboard history from disk."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []
    
    def save_history(self):
        """Save clipboard history to disk."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history[:self.max_items], f, indent=2)
        except Exception as e:
            print(f"Error saving clipboard history: {e}")
    
    def add_to_history(self, text: str):
        """Add text to clipboard history."""
        if not text or len(text) > 10000:
            return
        
        if text in [item['text'] for item in self.history]:
            self.history = [item for item in self.history if item['text'] != text]
        
        self.history.insert(0, {
            'text': text,
            'timestamp': time.time()
        })
        
        self.history = self.history[:self.max_items]
        self.save_history()
    
    def on_query(self, query: str):
        """Return clipboard history matching query."""
        if not query.lower().startswith('clip '):
            return None
        
        search_term = query[5:].strip().lower()
        
        results = []
        for item in self.history:
            text = item['text']
            preview = text.replace('\n', ' ')[:60]
            
            if not search_term or search_term in text.lower():
                results.append({
                    'type': 'clipboard',
                    'name': preview,
                    'subtitle': 'Clipboard History',
                    'action': text,
                    'icon': 'clipboard',
                    'score': 800
                })
        
        return results[:10]


def register(plugin_manager):
    """Register the plugin."""
    clipboard = ClipboardHistory(plugin_manager)
    plugin_manager.register_hook('on_query', clipboard.on_query)
