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
Web Search Shortcuts Plugin for SpotlightX
Extended web shortcuts beyond the built-in ones.
"""


class WebShortcuts:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        
        self.shortcuts = {
            'reddit ': ('Reddit', 'https://www.reddit.com/search/?q='),
            'tw ': ('Twitter', 'https://twitter.com/search?q='),
            'imdb ': ('IMDB', 'https://www.imdb.com/find?q='),
            'maps ': ('Google Maps', 'https://www.google.com/maps/search/'),
            'translate ': ('Google Translate', 'https://translate.google.com/?q='),
        }
    
    def on_query(self, query: str):
        """Parse additional web shortcuts."""
        for prefix, (name, url_template) in self.shortcuts.items():
            if query.lower().startswith(prefix):
                search_term = query[len(prefix):].strip()
                
                if search_term:
                    url = url_template + search_term.replace(' ', '+')
                    
                    return [{
                        'type': 'web',
                        'name': f"Search {name} for '{search_term}'",
                        'subtitle': name,
                        'action': url,
                        'icon': 'web',
                        'score': 850
                    }]
        
        return None


def register(plugin_manager):
    """Register the plugin."""
    shortcuts = WebShortcuts(plugin_manager)
    plugin_manager.register_hook('on_query', shortcuts.on_query)
