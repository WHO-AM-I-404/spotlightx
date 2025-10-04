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
Focus Mode Plugin for SpotlightX
Toggle focus/DND mode.
"""

import subprocess


class FocusMode:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.focus_enabled = False
    
    def toggle_focus(self):
        """Toggle focus mode."""
        self.focus_enabled = not self.focus_enabled
        
        try:
            if self.focus_enabled:
                subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '1'],
                             stderr=subprocess.DEVNULL)
            else:
                subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '0'],
                             stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
        return self.focus_enabled
    
    def on_query(self, query: str):
        """Handle focus mode queries."""
        if query.lower() not in ['focus', 'dnd', 'do not disturb']:
            return None
        
        status = "enabled" if self.focus_enabled else "disabled"
        
        return [{
            'type': 'action',
            'name': f"Focus Mode (currently {status})",
            'subtitle': 'Click to toggle',
            'action': 'toggle_focus',
            'icon': 'focus',
            'score': 900
        }]


def register(plugin_manager):
    """Register the plugin."""
    focus = FocusMode(plugin_manager)
    plugin_manager.register_hook('on_query', focus.on_query)
