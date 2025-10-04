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
Drag & Drop Integration Plugin for SpotlightX
Provides hints and helpers for drag and drop operations.
"""


class DragDrop:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
    
    def on_query(self, query: str):
        """Show drag and drop hints."""
        if query.lower() in ['drag', 'drop', 'move']:
            return [{
                'type': 'info',
                'name': 'Drag & Drop Support',
                'subtitle': 'Drag files from results to external applications',
                'action': '',
                'icon': 'drag',
                'score': 700
            }]
        
        return None


def register(plugin_manager):
    """Register the plugin."""
    drag_drop = DragDrop(plugin_manager)
    plugin_manager.register_hook('on_query', drag_drop.on_query)
