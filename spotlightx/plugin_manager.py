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
Plugin manager for SpotlightX.
Handles plugin loading, registration, and hook execution.
"""

import os
import json
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable


class PluginManager:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            config_dir = os.path.expanduser("~/.config/spotlightx")
        
        self.config_dir = Path(config_dir)
        self.plugins_dir = self.config_dir / "plugins"
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        
        self.plugins = {}
        self.hooks = {
            'on_query': [],
            'on_open': [],
            'on_startup': [],
            'on_shutdown': []
        }
    
    def load_plugin(self, plugin_path: Path) -> Optional[Dict[str, Any]]:
        """Load a single plugin from directory."""
        metadata_file = plugin_path / "plugin.json"
        plugin_file = plugin_path / "plugin.py"
        
        if not metadata_file.exists() or not plugin_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            plugin_id = metadata.get('id', plugin_path.name)
            
            if not metadata.get('enabled', False):
                print(f"Plugin {plugin_id} is disabled, skipping")
                return None
            
            spec = importlib.util.spec_from_file_location(plugin_id, plugin_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'register'):
                    module.register(self)
                
                plugin_data = {
                    'id': plugin_id,
                    'name': metadata.get('name', plugin_id),
                    'version': metadata.get('version', '1.0.0'),
                    'description': metadata.get('description', ''),
                    'module': module,
                    'metadata': metadata
                }
                
                self.plugins[plugin_id] = plugin_data
                print(f"Loaded plugin: {plugin_id}")
                return plugin_data
        except Exception as e:
            print(f"Error loading plugin from {plugin_path}: {e}")
            return None
    
    def load_all_plugins(self):
        """Load all plugins from plugins directory."""
        if not self.plugins_dir.exists():
            return
        
        for item in self.plugins_dir.iterdir():
            if item.is_dir():
                self.load_plugin(item)
    
    def register_hook(self, hook_name: str, callback: Callable):
        """Register a callback for a hook."""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(callback)
        else:
            print(f"Unknown hook: {hook_name}")
    
    def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all callbacks for a hook."""
        results = []
        
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    result = callback(*args, **kwargs)
                    if result is not None:
                        results.append(result)
                except Exception as e:
                    print(f"Error in hook {hook_name}: {e}")
        
        return results
    
    def get_plugin_config_dir(self, plugin_id: str) -> Path:
        """Get config directory for a plugin."""
        plugin_config_dir = self.plugins_dir / plugin_id
        plugin_config_dir.mkdir(parents=True, exist_ok=True)
        return plugin_config_dir
    
    def get_plugin_config(self, plugin_id: str) -> Dict[str, Any]:
        """Load plugin configuration."""
        config_file = self.get_plugin_config_dir(plugin_id) / "config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        
        return {}
    
    def save_plugin_config(self, plugin_id: str, config: Dict[str, Any]):
        """Save plugin configuration."""
        config_file = self.get_plugin_config_dir(plugin_id) / "config.json"
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving plugin config: {e}")
