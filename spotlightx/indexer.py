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
Indexer module for SpotlightX.
Scans .desktop files and file system, creates JSON cache.
"""

import os
import json
import time
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional
import configparser


class Indexer:
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/spotlightx")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.apps_cache_file = self.cache_dir / "apps.json"
        self.files_cache_file = self.cache_dir / "files.json"
        self.usage_cache_file = self.cache_dir / "usage.json"
        
        self.apps_data = []
        self.files_data = []
        self.usage_data = {}
        
        self.desktop_paths = [
            "/usr/share/applications",
            "/usr/local/share/applications",
            os.path.expanduser("~/.local/share/applications"),
            "/var/lib/snapd/desktop/applications",
            "/var/lib/flatpak/exports/share/applications",
            os.path.expanduser("~/.local/share/flatpak/exports/share/applications")
        ]
        
        self.file_roots = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Videos"),
            os.path.expanduser("~/Music"),
            os.path.expanduser("~"),
        ]
        
        self.indexing = False
        self.load_caches()
    
    def load_caches(self):
        """Load existing caches from disk."""
        try:
            if self.apps_cache_file.exists():
                with open(self.apps_cache_file, 'r') as f:
                    self.apps_data = json.load(f)
        except Exception as e:
            print(f"Error loading apps cache: {e}")
            self.apps_data = []
        
        try:
            if self.files_cache_file.exists():
                with open(self.files_cache_file, 'r') as f:
                    self.files_data = json.load(f)
        except Exception as e:
            print(f"Error loading files cache: {e}")
            self.files_data = []
        
        try:
            if self.usage_cache_file.exists():
                with open(self.usage_cache_file, 'r') as f:
                    self.usage_data = json.load(f)
        except Exception as e:
            print(f"Error loading usage cache: {e}")
            self.usage_data = {}
    
    def save_caches(self):
        """Save caches to disk."""
        try:
            with open(self.apps_cache_file, 'w') as f:
                json.dump(self.apps_data, f, indent=2)
        except Exception as e:
            print(f"Error saving apps cache: {e}")
        
        try:
            with open(self.files_cache_file, 'w') as f:
                json.dump(self.files_data, f, indent=2)
        except Exception as e:
            print(f"Error saving files cache: {e}")
        
        try:
            with open(self.usage_cache_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage cache: {e}")
    
    def parse_desktop_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Parse a .desktop file and extract relevant information."""
        try:
            config = configparser.ConfigParser(interpolation=None)
            config.read(filepath, encoding='utf-8')
            
            if 'Desktop Entry' not in config:
                return None
            
            entry = config['Desktop Entry']
            
            if entry.get('NoDisplay', 'false').lower() == 'true':
                return None
            
            if entry.get('Hidden', 'false').lower() == 'true':
                return None
            
            name = entry.get('Name', '')
            if not name:
                return None
            
            return {
                'type': 'app',
                'name': name,
                'exec': entry.get('Exec', ''),
                'icon': entry.get('Icon', ''),
                'comment': entry.get('Comment', ''),
                'categories': entry.get('Categories', '').split(';'),
                'path': filepath,
                'keywords': entry.get('Keywords', '').split(';')
            }
        except Exception as e:
            return None
    
    def index_applications(self) -> List[Dict[str, Any]]:
        """Index all .desktop files in standard locations."""
        apps = []
        
        for desktop_path in self.desktop_paths:
            if not os.path.exists(desktop_path):
                continue
            
            try:
                for filename in os.listdir(desktop_path):
                    if not filename.endswith('.desktop'):
                        continue
                    
                    filepath = os.path.join(desktop_path, filename)
                    app_data = self.parse_desktop_file(filepath)
                    
                    if app_data:
                        apps.append(app_data)
            except Exception as e:
                print(f"Error indexing {desktop_path}: {e}")
        
        return apps
    
    def index_files(self, max_depth: int = 4, max_files: int = 20000) -> List[Dict[str, Any]]:
        """Index files in configured root directories."""
        files = []
        file_count = 0
        
        for root_path in self.file_roots:
            if not os.path.exists(root_path):
                continue
            
            try:
                for root, dirs, filenames in os.walk(root_path):
                    depth = root.replace(root_path, '').count(os.sep)
                    if depth >= max_depth:
                        dirs[:] = []
                        continue
                    
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for filename in filenames:
                        if filename.startswith('.'):
                            continue
                        
                        filepath = os.path.join(root, filename)
                        
                        try:
                            stat = os.stat(filepath)
                            files.append({
                                'type': 'file',
                                'name': filename,
                                'path': filepath,
                                'mtime': stat.st_mtime,
                                'size': stat.st_size
                            })
                            
                            file_count += 1
                            if file_count >= max_files:
                                return files
                        except Exception:
                            continue
            except Exception as e:
                print(f"Error indexing files in {root_path}: {e}")
        
        return files
    
    def index_all(self):
        """Run full indexing of apps and files."""
        if self.indexing:
            print("Indexing already in progress")
            return
        
        self.indexing = True
        print("Starting full index...")
        
        try:
            self.apps_data = self.index_applications()
            print(f"Indexed {len(self.apps_data)} applications")
            
            self.files_data = self.index_files()
            print(f"Indexed {len(self.files_data)} files")
            
            self.save_caches()
            print("Index complete and saved")
        finally:
            self.indexing = False
    
    def index_all_async(self):
        """Run indexing in background thread."""
        thread = threading.Thread(target=self.index_all, daemon=True)
        thread.start()
        return thread
    
    def get_apps(self) -> List[Dict[str, Any]]:
        """Get all indexed applications."""
        return self.apps_data
    
    def get_files(self) -> List[Dict[str, Any]]:
        """Get all indexed files."""
        return self.files_data
    
    def record_usage(self, item_id: str):
        """Record usage of an item for ranking."""
        if item_id not in self.usage_data:
            self.usage_data[item_id] = {
                'count': 0,
                'last_used': 0
            }
        
        self.usage_data[item_id]['count'] += 1
        self.usage_data[item_id]['last_used'] = time.time()
        
        try:
            with open(self.usage_cache_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            print(f"Error saving usage data: {e}")
    
    def get_usage(self, item_id: str) -> Dict[str, Any]:
        """Get usage statistics for an item."""
        return self.usage_data.get(item_id, {'count': 0, 'last_used': 0})
