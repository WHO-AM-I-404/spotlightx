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
Timeline Plugin for SpotlightX
Records and displays activity timeline.
"""

import sqlite3
import time
from pathlib import Path


class Timeline:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        config_dir = self.pm.get_plugin_config_dir('timeline')
        self.db_path = config_dir / 'timeline.db'
        
        self.setup_database()
    
    def setup_database(self):
        """Setup SQLite database for timeline."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                item_type TEXT,
                timestamp REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_activity(self, item):
        """Record activity to timeline."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO activity (item_name, item_type, timestamp)
                VALUES (?, ?, ?)
            ''', (item.get('name', ''), item.get('type', ''), time.time()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error recording activity: {e}")
    
    def get_recent_activity(self, limit=10):
        """Get recent activity from timeline."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT item_name, item_type, timestamp
                FROM activity
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception:
            return []
    
    def on_open(self, item):
        """Record when item is opened."""
        self.record_activity(item)
    
    def on_query(self, query: str):
        """Show timeline when queried."""
        if query.lower() not in ['timeline', 'history', 'recent']:
            return None
        
        recent = self.get_recent_activity(10)
        
        results = []
        for name, item_type, timestamp in recent:
            time_ago = int((time.time() - timestamp) / 60)
            results.append({
                'type': 'info',
                'name': name,
                'subtitle': f"{item_type} — {time_ago} minutes ago",
                'action': '',
                'icon': 'timeline',
                'score': 800
            })
        
        return results


def register(plugin_manager):
    """Register the plugin."""
    timeline = Timeline(plugin_manager)
    plugin_manager.register_hook('on_open', timeline.on_open)
    plugin_manager.register_hook('on_query', timeline.on_query)
