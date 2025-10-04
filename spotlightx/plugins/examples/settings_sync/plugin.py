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
Settings Sync Plugin for SpotlightX
Export and import settings for backup/sync.
"""

import json
import os
from pathlib import Path


class SettingsSync:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.config_dir = Path(os.path.expanduser("~/.config/spotlightx"))
    
    def export_settings(self):
        """Export all settings to JSON."""
        try:
            settings = {
                'version': '1.0.0',
                'plugins': {}
            }
            
            for plugin_id in self.pm.plugins:
                config = self.pm.get_plugin_config(plugin_id)
                settings['plugins'][plugin_id] = config
            
            export_path = self.config_dir / 'settings_export.json'
            
            with open(export_path, 'w') as f:
                json.dump(settings, f, indent=2)
            
            return str(export_path)
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return None
    
    def on_query(self, query: str):
        """Handle settings sync queries."""
        if query.lower() in ['sync', 'export settings', 'backup']:
            return [{
                'type': 'action',
                'name': 'Export Settings',
                'subtitle': 'Backup your SpotlightX configuration',
                'action': 'export',
                'icon': 'sync',
                'score': 800
            }]
        
        return None


def register(plugin_manager):
    """Register the plugin."""
    sync = SettingsSync(plugin_manager)
    plugin_manager.register_hook('on_query', sync.on_query)
