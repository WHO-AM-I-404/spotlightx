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
Translator Plugin for SpotlightX
Provides quick translation via web services.
"""


class Translator:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.config = self.pm.get_plugin_config('translator')
    
    def on_query(self, query: str):
        """Translate queries starting with 'tr '."""
        if not query.lower().startswith('tr '):
            return None
        
        text = query[3:].strip()
        
        if not text:
            return None
        
        url = f"https://translate.google.com/?sl=auto&tl=en&text={text.replace(' ', '%20')}"
        
        return [{
            'type': 'web',
            'name': f"Translate: {text[:40]}...",
            'subtitle': 'Google Translate',
            'action': url,
            'icon': 'translate',
            'score': 850
        }]


def register(plugin_manager):
    """Register the plugin."""
    translator = Translator(plugin_manager)
    plugin_manager.register_hook('on_query', translator.on_query)
