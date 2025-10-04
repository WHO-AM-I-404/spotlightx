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
File Preview Plugin for SpotlightX
Shows quick preview of file content.
"""

import os


class FilePreview:
    def __init__(self, plugin_manager):
        self.pm = plugin_manager
        self.preview_extensions = {
            'text': ['.txt', '.md', '.py', '.js', '.json', '.xml', '.html', '.css'],
            'image': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg'],
            'pdf': ['.pdf']
        }
    
    def get_file_type(self, filepath):
        """Determine file type from extension."""
        ext = os.path.splitext(filepath)[1].lower()
        
        for file_type, extensions in self.preview_extensions.items():
            if ext in extensions:
                return file_type
        
        return None
    
    def preview_text_file(self, filepath, max_lines=5):
        """Preview text file content."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [f.readline().strip() for _ in range(max_lines)]
                return ' '.join(lines)[:100]
        except Exception:
            return "Unable to preview"
    
    def on_query(self, query: str):
        """Add preview info to file results."""
        if query.lower().startswith('preview '):
            filename = query[8:].strip()
            
            if os.path.exists(filename):
                file_type = self.get_file_type(filename)
                
                if file_type == 'text':
                    preview = self.preview_text_file(filename)
                    
                    return [{
                        'type': 'file',
                        'name': os.path.basename(filename),
                        'subtitle': preview,
                        'action': filename,
                        'icon': 'file',
                        'score': 850
                    }]
        
        return None


def register(plugin_manager):
    """Register the plugin."""
    preview = FilePreview(plugin_manager)
    plugin_manager.register_hook('on_query', preview.on_query)
